# from bson.json_util import dumps

# def xyz():
#     from pymongo import MongoClient
#     client = MongoClient("mongos8", 27017)
#     db = client['my_db']
#     coll = db['people']
#     # for x in collection.find({}):
#     #     print(x)
#     data = {"age":54}
#     print(coll.find(data))
#     # resp = dumps(coll.find(data))
#     x = db.list_collection_names()
#     print(x)
#     # print(list(x))
#     return "yy"
# xyz()


# import multiprocessing

# def xyz(key, return_list):
#     # lst = []
#     print(key)
#     for i in range(10):
#         # i["shard"] = shard
#         return_list.append(i)
#     # return lst

# def abc():
#     manager = multiprocessing.Manager()
#     return_list = manager.list()
#     jobs = []
#     for shard in range(6):
#         process = multiprocessing.Process(target=xyz, args=(5, return_list))
#         jobs.append(process)
#         process.start()
#         # lst.extend(data_shard_i)

#     for j in jobs:
#         j.join()
    
#     return list(return_list)
# print(abc())

# from app import search_test
# for i in range(1,5001):
#     x = search_test("age",i)
#     x = str(x)
#     if x not in '':
#         print(x)
#     with open('analytics.txt', 'w') as the_file:
#         the_file.write(str(x))

# print(search_test("age", 6))