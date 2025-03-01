from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import CollectionInvalid
def connect(host, port=27017):
    client = MongoClient(host, port)
    return client
def get_db(client, db='test_database'):
    return client[db]
def get_collection(client, db_name='test_database', collection='posts'):
    return client[db_name][collection]
def create_collections(client, db_name, prefix='posts', count=1000):
    db = get_db(client, db_name)
    for i in range(count):
        collection_name = f'{prefix}{i}'
        try:
            db.create_collection(collection_name)
            print(f'dbname: {db_name} collection {collection_name} - created')
        except CollectionInvalid as e:
            print(f'dbname: {db_name} collection {collection_name} - already exists')
    return
def create_databases(client, prefix='test_database', count=10,
                     collection_prefix='posts', collection_count=100):
    for i in range(count):
        db_name = f'{prefix}{i}'
        create_collections(client, db_name, collection_prefix, collection_count)

if __name__ == '__main__':
    client = connect('10.3.59.156')
    dbs = client.list_database_names()
    for db in dbs:
        if 'test_database' in db:
            client.drop_database(db)