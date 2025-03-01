import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A program to populate dbs in mongodb',
        usage='python3 pumper.py --host 10.14.69.121 --db_name prodsb21\
                        --user sys --password cohesity --total_size 1G \
                        --datafile_size 200M --batch_size 200000 ')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')