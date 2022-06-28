# from crypt import methods
from itertools import count
from flask import Flask,request
import json
from populate import init
from pymongo import MongoClient
import index
from threading import Thread
import threading
from requests import post, get
from index import BTree;
from bson.json_util import dumps
import time
from collections import Counter

app = Flask(__name__)

N = 11

shards = ["mongos"+str(x) for x in range(1, N)]

collections = {}

indices = []

trees = {}

@app.route('/startup', methods=['GET'])
def startup():
    global indices
    global trees
    global collections
    global shards
    # make connections, db and map collections to shards
    dbconfig = request.get_json()
    if not dbconfig:
        for shard in shards:
            client = MongoClient(shard, 27017)
            db = client.my_db
            collection = db.people
            collections[shard] = collection
            collection.create_index('country')
            collection.create_index('age')
            collection.create_index('salary')


        indices = ["age", "salary", "country"]
        trees = {
            "age": BTree(50, -1),
            "salary": BTree(50, -1),
            "country": BTree(50, " ")
        }
        init(collections, trees)
        # B.print_tree(B.root)
        trees["age"].print_tree(trees["age"].root)
        trees["salary"].print_tree(trees["salary"].root)
        trees["country"].print_tree(trees["country"].root)
        return "db with people initialized"
    else:
        # use pymongo to create db, create collection, create index, 
        for shard in shards:
            client = MongoClient(shard, 27017)
            db = client[dbconfig["db_name"]]
            collection = db[dbconfig["collection_name"]]
            collections[shard] = collection
            for index in dbconfig["index_list"]:
                collection.create_index(index["index_key"])
        
        for index in dbconfig["index_list"]:
            indices.append(index["index_key"])
            trees[index["index_key"]] = BTree(20, index["default"])
        return "random db initialization complete"
    

# Startup procedure - 
# 1. make connections and then on to collections
# 2. generate people data and associate random node with it
# 3. insert the data in index
# 4. send write request to that particular mongo node
# do this `100 times`

class ThreadWithReturnValue(Thread):
    '''
    A custom Thread class which allows 
    '''
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return


root = 0 # initialize root with index tree root. maybe for now we can move the init part over here.
nodes = []

def initializer():
    pass

@app.route('/test', methods=['GET'])
def test():
    '''
    test
    '''
    print("success")
    return "success 200 main"

@app.route('/execute', methods=['GET'])
def query_collector():
    '''
    Recieve query string
    call function to get node list
    call function to send request to all nodes and collect all the responses and send back
    return the consolidated response
    '''
    t1 = time.time()
    data = request.get_json()
    keys = list(data.keys())
    key = keys[0]
    x = nodeSelector(data, key)
    if x is False:
        return "no data found"
    n_nodes = len(x.nodes)
    answer = consildator(data, x.nodes)
    t2 = time.time()
    answer.append({"execution time": str(t2-t1)})
    answer.append({"number of nodes queried": str(n_nodes)})
    print("Execution time: {}".format(t2-t1))
    return json.dumps(answer)

def nodeSelector(data, key):
    '''
    Recieve a request, use the index to determine subset of nodes to send the data to.
    '''
    global shards
    if key not in indices:
        return shards 
    value = data[key] 
    x = trees[key].search_key(value)
    return x

def consildator(data, nodes):
    '''
    asynchronously send requests to all the nodes, collect response and consolidate in one
    '''
    req_threads = []
    print(nodes)
    for i, x in enumerate(nodes):
        req_threads.append(ThreadWithReturnValue(target=query_forward, args=(data, x)))
        req_threads[i].start()
    answers = []
    print(answers)
    for x in req_threads:
        answers.append(x.join())  
    return answers

def query_forward(data, node):
    '''
    forward query to individual node and give back the response
    '''
    # send request to single node app
    coll = collections[node]
    resp = dumps(coll.find(data))
    # print(resp)
    return resp


@app.route('/write', methods=['GET'])
def write_query():
    '''
    take the data from the json
    query different indices and obtain the different nodes
    select the node with max frequency -- if no nodes then just select random node
    insert into the index
    insert data in that node
    '''

    data = request.get_json()
    node = poll(data)
    insert_index(data, node)
    result = collections[node].insert_one(data)

    return "write was successful in node {}".format(node)


def insert_index(data, node):
    for index in indices:
        trees[index].insert((data[index], node))
    

def poll(data):
    '''
    take data and then poll all of the indices for the prefered node
    '''
    possible_nodes = []
    for index in indices:
        val = data[index]
        x = trees[index].search_key(val)
        if x is False:
            continue
        possible_nodes.extend(x.nodes)
    return Counter(possible_nodes).most_common(1)[0][0]


    
if __name__ == '__main__':
    print("starting main...")
    # run() method of Flask class runs the application 
    # on the local development server.
    # startup()

    app.run(host="0.0.0.0", port=8080, debug=True)



# # startup api

# # call to initialize a new database
# # send a json response - 
# # {
# #     "db": db_name,
# #     "collection": collection_name,
# #     "index list": [{
# #       "index key": key,
#         "default value": val
# # }, "index2"]
# # }
# if its {
#     "db": default
# }
# then go ahead with people database and populate it else just make the connection, index  and leave it as it is