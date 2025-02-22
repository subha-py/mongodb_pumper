import random
import sys
from string import ascii_letters
import datetime
from pprint import pprint
from threading import Lock
import concurrent.futures
from utils.connect import get_collection, get_db, connect
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

def process_batch(connection, batch_size,
                batch_number,
                lock, docs, number_of_batches):
    if not docs:
        docs = create_random_docs(batch_size)
    collection = get_collection(connection)
    print(f'{batch_number}/{number_of_batches}: inserting {batch_size} docs')
    collection.insert_many(docs)
    print(f'{batch_number}/{number_of_batches}: successfully inserted '
          f'{batch_size} docs')
    return
def pump_data(connection, db_name=None, total_size=None, batch_size=100,
                  max_threads=128):
    total_docs_required = 10000 #todo
    number_of_batches = total_docs_required // batch_size
    future_to_batch = {}
    workers = min(max_threads, number_of_batches)
    print('number of workers - {}'.format(workers))
    lock = Lock()
    with concurrent.futures.ThreadPoolExecutor(
            max_workers=workers) as executor:
        for batch_number in range(1, number_of_batches + 1):
            arg = (
                connection, batch_size,
                batch_number,
                lock, None, number_of_batches)
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
            # todo: handle here sequentially for error batches

    return result




if __name__ == '__main__':
    connection = connect('10.3.59.156')
    pump_data(connection)