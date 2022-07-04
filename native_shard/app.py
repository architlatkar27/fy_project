from crypt import methods
from unittest import result
from urllib import response
from flask import Flask, jsonify,request
import pymongo
from pymongo import MongoClient
import json
from bson.json_util import loads, dumps
from time import process_time
from faker import Faker
from random import randrange
from time import process_time

app = Flask(__name__)

#temp = "mongos1"
# temp1 = "localhost"
# shards = ["mongos1", "mongos2", "mongos3", "mongos4", "mongos5", "mongos6"]
shard = "router01"
shards_cnt = 9

def create_names(fake, shard_name, coll_ptr):
    cnt = 0
    for x in range(100*shards_cnt):
        genName = fake.first_name()
        genSurname = fake.last_name()
        genJob = fake.job()
        genCountry = fake.country()
        genSalary = randrange(10000, 100000, 1000)
        genAge = randrange(1, 9)
        t1_start = process_time() 
        
        result = coll_ptr.insert_one(
            {
                'name': genName,
                'surname': genSurname,
                'job': genJob,
                'country': genCountry,
                'salary': genSalary,
                'age': genAge
                }
            )
        
        t2_start = process_time() 
        cnt += (t2_start - t1_start)
    return cnt/100


@app.route('/test', methods=['GET'])
def test():
    '''
    test
    '''
    print("success")
    return "success 200 native-shard"

@app.route('/insert_bulk', methods=['GET'])
def insert_bulk():
    # data = request.form
    # # result = my_collection.find(data)

    client = MongoClient(shard, 27017)
    db = client.my_db
    coll = db.people
    # coll.create_index('age')

    fake = Faker()
    avg_tm = create_names(fake, shard, coll)
    resp = "bulk insert success | resp time: " + str(avg_tm)
    return resp

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    
    query_key = data["query_key"]
    query_val = data["query_val"]
    client = MongoClient(shard, 27017)
    db = client.my_db
    coll = db.people

    res = []
    t1_start = process_time() 
    for i in coll.find({query_key:query_val}):
        res.append(i)
    t2_start = process_time() 
    res.append({"response time": (t2_start-t1_start)})
    return str(res)

if __name__ == '__main__':
    print("starting single-node...")
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(host="0.0.0.0", port=8080, debug=True)
