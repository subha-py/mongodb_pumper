from pymongo import MongoClient
from pprint import pprint
def connect(host, port=27017):
    client = MongoClient(host, port)
    return client
def get_db(client, db='test_database'):
    return client[db]
def get_collection(db, collection='posts'):
    return client[db][collection]

if __name__ == '__main__':
    client = connect('10.3.59.156')
    collection = get_collection(client)
    pprint(collection.find_one())