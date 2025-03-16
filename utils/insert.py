import random
import sys
from string import ascii_letters
import datetime
import concurrent.futures
from utils.connect import get_collection, connect, create_databases
from utils.memory import get_number_of_rows_from_size
sys.path.append('/root/mongodb_pumper/utils')
sys.path.append('/root/mongodb_pumper')
def create_random_doc():
    toggle = random.choice([True, False])
    task_number = random.randint(1, sys.maxsize)
    random_string = ''.join(random.choices(ascii_letters, k=10))
    random_texts = ''.join(random.choices(ascii_letters, k=200))
    post = {
        "author": random_string,
        "text": random_texts,
        "task_id": task_number,
        "date": datetime.datetime.now(tz=datetime.timezone.utc),
        "toggle": toggle
    }
    return post


def create_random_docs(batch_size):
    docs = []
    for i in range(batch_size):
        docs.append(create_random_doc())
    return docs

def process_batch(ip, batch_size,
                batch_number,
                docs, number_of_batches, db_name, collection_name):
    if not docs:
        docs = create_random_docs(batch_size)
    connection = connect(ip)
    collection = get_collection(connection, db_name, collection_name)
    print(f'{batch_number}/{number_of_batches}: inserting {batch_size} docs')

    collection.insert_many(docs)
    print(f'{batch_number}/{number_of_batches}: successfully inserted '
          f'{batch_size} docs')
    return
def pump_data(ip, total_size, batch_size=10000,
                  max_threads=128, create_database=False):
    number_of_batches = get_number_of_rows_from_size(total_size) // batch_size
    future_to_batch = {}
    workers = min(max_threads, number_of_batches)
    connection = connect(ip)
    if create_database:
        create_databases(connection)
    dbs = []
    for db in connection.list_database_names():
        if 'test_database' in db:
            dbs.append(db)
    collections = connection[dbs[0]].list_collection_names()
    print('number of workers - {}'.format(workers))
    with concurrent.futures.ThreadPoolExecutor(
            max_workers=workers) as executor:
        for batch_number in range(1, number_of_batches + 1):
            arg = (
                ip, batch_size,
                batch_number, None, number_of_batches, random.choice(dbs),
                random.choice(collections))
            future_to_batch[
                executor.submit(process_batch, *arg)] = batch_number

    result = []
    for future in concurrent.futures.as_completed(future_to_batch):
        batch_number = future_to_batch[future]
        try:
            res = future.result()
            if not res:
                result.append(batch_number)
        except Exception as exc:
            print("%r generated an exception: %s" % (batch_number, exc))
    return result

if __name__ == '__main__':
    # connection = connect('10.3.59.157')
    ip = '10.3.59.157'
    pump_data(ip, '2T', create_database=False)