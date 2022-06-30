## use this script to populate mongodb database with fake people data
from pymongo import MongoClient
from faker import Faker
from random import randrange
import time 
from time import process_time

def init(collections, trees):
    fake = Faker()
    cnt = 0
    for shard_name, coll_ptr in collections.items():
        cnt += create_names(fake, shard_name, coll_ptr, trees)
    return cnt/len(list(collections.items()))
def create_names(fake, shard_name, coll_ptr, trees):
    cnt = 0
    for x in range(10000):
        genName = fake.first_name()
        genSurname = fake.last_name()
        genJob = fake.job()
        genCountry = fake.country()
        genSalary = randrange(10000, 100000, 1000)
        genAge = randrange(1, 5000)
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
        
        trees["age"].insert(genAge, shard_name)
        t2_start = process_time() 
        cnt += (t2_start - t1_start)
    return cnt/100
        # trees["salary"].insert((genSalary, cont))
        # trees["country"].insert((genCountry, cont))
        # B.insert(genJob,coll);
        # print('id: ' + str(result.inserted_id) + ' name: ' + genName)



# if __name__ == '__main__':
#     fake = Faker()
#     create_names(fake)