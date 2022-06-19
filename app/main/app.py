# from crypt import methods
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


app = Flask(__name__)

shards = ["mongos1", "mongos2", "mongos3", "mongos4", "mongos5", "mongos6"]

collections = {}

B = BTree(17)

def startup():

    # make connections, db and map collections to shards
    for shard in shards:
        client = MongoClient(shard, 27017)
        db = client.my_db
        collection = db.people
        collections[shard] = collection

    
    init(collections, B)
    B.print_tree(B.root)
    

# Startup procedure - 
# 1. make connections and then on to collections
# 2. generate people data and associate random node with it
# 3. insert the data in index
# 4. send write request to that particular mongo node
# do this `100 times`

class ThreadWithReturnValue(Thread):
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
    data = request.get_json()
    x = nodeSelector(data)
    if x is False:
        return "no data found"
    answer = consildator(data, x.nodes)
    return json.dumps(answer)
    pass

def nodeSelector(data):
    '''
    Recieve a request, use the index to determine subset of nodes to send the data to.
    '''
    value = data["age"]# check how to get the data.
    print(value)
    print(type(value))
    
    x = B.search_key(value)
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
    
    # need to see how to combine the answers returned over here

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


if __name__ == '__main__':
    print("starting main...")
    # run() method of Flask class runs the application 
    # on the local development server.
    startup()
    app.run(host="0.0.0.0", port=8080, debug=True)