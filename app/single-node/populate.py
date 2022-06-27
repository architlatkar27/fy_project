## use this script to populate mongodb database with fake people data
from pymongo import MongoClient
from faker import Faker
import time 

client = MongoClient('localhost', 27017)
db = client.my_db

def create_names(fake):
    for x in range(10000):
        genName = fake.first_name()
        genSurname = fake.last_name()
        genJob = fake.job()
        genCountry = fake.country()

        result = db.people.insert_one(
            {
                'name': genName,
                'surname': genSurname,
                'job': genJob,
                'country': genCountry
                }
            )

        print('id: ' + str(result.inserted_id) + ' name: ' + genName)
        time.sleep(1)
        db.people.create_index('name')
        db.people.create_index('country')
    _ = db.people.index_information()
if __name__ == '__main__':
    fake = Faker()
    create_names(fake)