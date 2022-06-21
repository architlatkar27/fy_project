## use this script to populate mongodb database with fake people data
from pymongo import MongoClient
from faker import Faker
from random import randrange
import time 

def init(collections, trees):
    fake = Faker()
    
    for k, v in collections.items():
        create_names(fake, k, v, trees)




def create_names(fake, cont, coll, trees):
    for x in range(100):
        genName = fake.first_name()
        genSurname = fake.last_name()
        genJob = fake.job()
        genCountry = fake.country()
        genSalary = randrange(10000, 100000)
        genAge = randrange(1, 100)
        result = coll.insert_one(
            {
                'name': genName,
                'surname': genSurname,
                'job': genJob,
                'country': genCountry,
                'salary': genSalary,
                'age': genAge
                }
            )
        trees["age"].insert((genAge, cont))
        trees["salary"].insert((genSalary, cont))
        # B.insert(genJob,coll);
        # print('id: ' + str(result.inserted_id) + ' name: ' + genName)



# if __name__ == '__main__':
#     fake = Faker()
#     create_names(fake)