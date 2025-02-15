import random
import sys
from string import ascii_letters
import datetime
from pprint import pprint

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


def get_docs(batch_size):
    docs = []
    for i in range(batch_size):
        docs.append(create_random_doc())
    return docs


if __name__ == '__main__':
    docs = get_docs(3)
    pprint(docs)
