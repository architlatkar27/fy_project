# from crypt import methods
from concurrent.futures import process
import imp
from itertools import count
import re
from this import s
from flask import Flask,request
import json
from populate import init
from pymongo import MongoClient
# import index
from cus_tree import Tree
from threading import Thread
import threading
from requests import post, get
from index import BTree;
from bson.json_util import dumps
from time import process_time
import multiprocessing

app = Flask(__name__)

N = 9

shards = ["mongos"+str(x) for x in range(1, N+1)]

collections = {}

indices = []

trees = {}

@app.route('/startup', methods=['GET'])
def startup():
    global indices
    global trees
    global collections
    global shards
    for shard in shards:
        client = MongoClient(shard, 27017)
        db = client.my_db
        collection = db.people
        collections[shard] = collection
        # collection.create_index('country')
        collection.create_index('age')
        # collection.create_index('salary')


    indices = ["age"]
    # indices = ["age", "salary", "country"]
    trees = {
        "age": Tree("age"),
        # "salary": BTree(30, -1),
        # "country": BTree(30, " ")
    }
    # t1_start = process_time() 

    avg_tm = init(collections, trees)
    # t2_start = process_time() 
    # avg_tm = (t2_start - t1_start)
    # B.print_tree(B.root)
    # trees["age"].print_tree()
    # trees["salary"].print_tree(trees["salary"].root)
    # trees["country"].print_tree(trees["country"].root)
    return "db with people initialized, avg_time for each write: " + str(avg_tm)

# Startup procedure - 
# 1. make connections and then on to collections
# 2. generate people data and associate random node with it
# 3. insert the data in index
# 4. send write request to that particular mongo node
# do this `100 times`

@app.route('/test', methods=['GET'])
def test():
    '''
    test
    '''
    print("success")
    x = []
    for i in range(1, 6001):
        temp = search_test("age", i)

        with open('analytics.txt', 'a') as the_file:
            the_file.write(temp)

    return "success 200 main"

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query_key = data["query_key"]
    query_val = data["query_val"]
    # print(list(trees.keys()))
    if query_key in list(trees.keys()):
        idx = query_key
        tree = trees[idx]
        t1_start = process_time() 
        shards_lst = list(tree.search_key(query_val))
        res = search_shards(query_key, query_val, shards_lst)
        t2_start = process_time() 
        sz = len(res)
        # res.append({"time_elapsed":(t2_start-t1_start), "result size":(sz), "no of shards queried":len(shards_lst)})
        x = ({"time_elapsed":(t2_start-t1_start), "result size":(sz), "no of shards queried":len(shards_lst)})
        return str(x)
    else:
        return "index not found " + str(list(trees.keys())) 

    print("success")
    return "success 200 main"

def search_test(query_key, query_val):    
    if query_key in list(trees.keys()):
        idx = query_key
        tree = trees[idx]
        t1_start = process_time() 
        shards_lst = list(tree.search_key(query_val))
        res = search_shards(query_key, query_val, shards_lst)
        t2_start = process_time() 
        sz = len(res)
        # res.append({"time_elapsed":(t2_start-t1_start), "result size":(sz), "no of shards queried":len(shards_lst)})
        x = str(t2_start-t1_start) + "," + str(sz) + "," + str(len(shards_lst)) + "\n"
        return x
    return ""


@app.route('/reindex', methods=['POST'])
def reindex():
    data = request.get_json()
    idx_key = data["index_key"]
    trees[idx_key] = Tree(idx_key)        

    for shard in shards:
        local_client = MongoClient(shard, 27017)
        local_coll = local_client.my_db.people
        local_coll.create_index((idx_key))
        for i in local_coll.find({}):
            trees[idx_key].insert(i[idx_key], shard)
    # trees[idx_key].print_tree()
    # print(list(trees.keys()))
    print("success")
    return "success 200 main"

def search_shard(key, val, shard, return_list):
    # lst = []
    print("Helllllo")
    local_client = MongoClient(shard, 27017)
    local_coll = local_client.my_db.people
    # collection = db.people
    for i in local_coll.find({key:val}):
        i["shard"] = shard
        # print(i)
        return_list.append(i)
    # return lst

def search_shards(key, val, shards):
    manager = multiprocessing.Manager()
    return_list = manager.list()
    jobs = []
    for shard in shards:
        # data_shard_i = search_shard(key, val, shard)
        # coll_shard = collections[shard]
        process = multiprocessing.Process(target=search_shard, args=(key, val, shard, return_list))
        jobs.append(process)
        process.start()
        # lst.extend(data_shard_i)

    for j in jobs:
        j.join()
    # print(return_list)
    return return_list

    
if __name__ == '__main__':
    print("starting main...")
    # run() method of Flask class runs the application 
    # on the local development server.
    # startup()

    app.run(host="0.0.0.0", port=8080, debug=True)
