from pymongo import MongoClient
from pprint import pprint
def connect(host, port=27017):
    client = MongoClient(host, port)
    return client
def get_db(client, db='test_database'):
    return client[db]
def get_collection(client, db_name='test_database', collection='posts'):
    return client[db_name][collection]

if __name__ == '__main__':
    client = connect('10.3.59.156')
    collection = get_collection(client, )
    pprint(collection.find_one())