# from crypt import methods
import imp
from itertools import count
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
import time
from collections import Counter


app = Flask(__name__)

N = 10

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
    init(collections, trees)
    # B.print_tree(B.root)
    trees["age"].print_tree()
    # trees["salary"].print_tree(trees["salary"].root)
    # trees["country"].print_tree(trees["country"].root)
    return "db with people initialized"

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
    # print("success")
    # return "success 200 main"

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    query_key = data["query_key"]
    query_val = data["query_val"]
    if query_key in list(trees.keys()):
        idx = query_key
        tree = trees[idx]
        shards_lst = list(tree.search_key(query_val))
        print(shards_lst)
        return str(search_shards(query_key, query_val, shards_lst))
    else:
        return "index not found"

    print("success")
    return "success 200 main"

def search_shard(key, val, shard):
    lst = []
    for i in collections[shard].find({key:val}):
        i["shard"] = shard
        lst.append(i)
    return lst

def search_shards(key, val, shards):
    lst = []
    for shard in shards:
        lst.extend(search_shard(key, val, shard))
    return lst

    
if __name__ == '__main__':
    print("starting main...")
    # run() method of Flask class runs the application 
    # on the local development server.
    # startup()

    app.run(host="0.0.0.0", port=8080, debug=True)
