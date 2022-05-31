from crypt import methods
from urllib import response
from flask import Flask, jsonify,request
import pymongo
from pymongo import MongoClient
import json

app = Flask(__name__)

client = MongoClient("localhost", 27017)

db = client.my_db
my_collection = db.people
query_string = "find()"
# print(db.command(query_string, "people"))
# @app.route('/execute', methods=['GET'])
# def query_executor():
#     '''
#     Takes in a query string and executes it as it is
#     '''
#     query_string = request.args.get('query')
#     query_string = "people.find()"
#     print(db.command(query_string))

@app.route('/insert', methods=['POST'])
def insert():
    '''
    Insert document into mongodb
    '''
    data = request.form
    print(data['name'])
    data = jsonify(data)
    print(data)
    print(type(data))
    return "got data"
    #my_collection.insert_one()

if __name__ == '__main__':
  
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()