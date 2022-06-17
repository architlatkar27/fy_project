from crypt import methods
from unittest import result
from urllib import response
from flask import Flask, jsonify,request
import pymongo
from pymongo import MongoClient
import json
from bson.json_util import loads, dumps

app = Flask(__name__)

temp = "mongos1"
temp1 = "localhost"
shards = ["mongos1", "mongos2", "mongos3", "mongos4", "mongos5", "mongos6"]
client = MongoClient(temp, 27017)

db = client.my_db
my_collection = db.people



@app.route('/test', methods=['GET'])
def test():
    '''
    test
    '''
    print("success")
    return "success 200 single-node"

@app.route('/execute', methods=['GET'])
def query_executor():
    '''
    collect form data and execute find on it
    '''
    data = request.form
    result = my_collection.find(data)
    resp = dumps(result)
    return resp

@app.route('/insert', methods=['POST'])
def insert():
    '''
    Insert document into mongodb
    '''
    data = request.get_json(force=True)
    # data = { "_id": 5,
    #       "name": "Raju",
    #       "Roll No": "1005",
    #       "Branch": "CSE"}
    my_collection.insert_one(data)
    return data

if __name__ == '__main__':
    print("starting single-node...")
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host="0.0.0.0", port=8080, debug=True)

