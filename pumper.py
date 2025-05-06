import argparse
from utils.insert import pump_data
from utils.connect import connect

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A program to populate dbs in mongodb',
        usage='python3 pumper.py --host st-monog-1')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # add arguments here
    required.add_argument('--host', help='ip/hostname of the db', type=str, required=True)
    optional.add_argument('--size', help='size of data will be inserted(default 100G)', type=str, default='100G')
    optional.add_argument('--batch_size', help='number of rows to inserted at a time', type=int, default=10000)
    optional.add_argument('--threads', help='threads to run data pump', type=int, default=2)

    # parsing
    result = parser.parse_args()

    # starting data pump
    connection = connect(result.host)
    pump_data(connection=connection, total_size=result.size,batch_size=result.batch_size,max_threads=result.threads,
        create_database=True)