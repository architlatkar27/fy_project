from crypt import methods
from unittest import result
from urllib import response
from flask import Flask, jsonify,request
import pymongo
from pymongo import MongoClient
import json
from bson.json_util import loads, dumps

app = Flask(__name__)

client = MongoClient("localhost", 27017)

db = client.my_db
my_collection = db.people



@app.route('/test', methods=['GET'])
def test():
    '''
    test
    '''
    print("success")
    return "success"

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
    data = request.form
    doc = data.to_dict()
    return "got data"
    #my_collection.insert_one()

if __name__ == '__main__':
    print("starting...")
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host="0.0.0.0", port=8080)

