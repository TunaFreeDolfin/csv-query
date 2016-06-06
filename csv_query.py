import argparse
import csv
import sys

from config import store
from models.person import Person
from models.person_index import PersonIndex


def _validate_headers(headers):
    '''
    Validates the header row of the CSV is what we expect
    :param headers: The header row as a list
    :return:
    '''
    expected_format = ['ID', 'First', 'Last', 'Age', 'GithubAcct', 'Date of 3rd Grade Graduation']
    for i in range(0, len(headers) - 1):
        if headers[i] != expected_format[i]:
            raise ValueError("The CSV format is incorrect. Expected [{}]".format(','.join(expected_format)))


def _parse_csv(csv_path):
    '''
    Parses the CSV file
    :param csv_path: path to CSV, including filename
    :return:
    '''
    print "Reading data, please wait..."
    person_index = PersonIndex(store)
    with open(csv_path) as csvfile:
        row_reader = csv.reader(csvfile)
        headers = row_reader.next()
        _validate_headers(headers)
        for row in row_reader:
            person = Person(*row, store=store)
            person_index.add_person_to_index(person)
    print "Finished reading data"


def _setup_parser():
    '''
    Sets up the parser
    :return:
    '''
    parser = argparse.ArgumentParser(description='Allows querying of passed in CSV file')
    parser.add_argument('csv_path', type=str, help='the path to the CSV file to query')
    return parser.parse_args()


def _main_loop():
    '''
    The main loop that waits for input and acts on it
    :return:
    '''
    person_index = PersonIndex(store)
    run = True
    while run:
        print "Enter the last name, 'all' to get a sorted list, or 'exit' to quit:"
        line = sys.stdin.readline()
        if line.lower().strip() == 'exit':
            run = False
        elif line.lower().strip() == 'all':
            for person in person_index.all():
                print person.__str__()
        else:
            print "IDs found for that last name:"
            print person_index.get_ids_by_last_name(line.strip())
    # Flush redis so that subsequent sessions don't have data from previous ones
    store.flushall()


if __name__ == '__main__':
    args = _setup_parser()
    _parse_csv(args.csv_path)
    _main_loop()
