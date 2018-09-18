import sys
sys.path.append("/afs/cern.ch/user/m/mpetrika/private/cms/task/")

import csvFileReader, csvDataConverter
import argparse
from database.dbSetup import get_db_controller

def import_from_file(file_name):
    raw_data =_read_file(file_name)
    data = _process_data(raw_data)
    _save_to_db(data)
    

def _read_file(file_name: str) -> iter:
    return csvFileReader.read_file(file_name)

def _process_data(raw_data: iter) -> iter:
    csv_data = csvDataConverter.from_row_to_record(raw_data)
    for run, data in csv_data.items():
        for params, scores in data.items():
            yield dict([run]), dict(params[:]), scores

def _save_to_db(data: iter):
    records = get_db_controller().get_all_loaded_run_identifiers()
    identifiers = list(map(lambda x:x["identifier"], records))
    for identifier, params, scores in data:
        if (identifier in identifiers):
            get_db_controller().update_user_score(identifier, params, scores)
            print(f"saved: {identifier} {params}")
        else:
            print(f"not found in database: {identifier} {params}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Imports data from csv file')
    parser.add_argument('file', help='name of file from which data will be')
    args = parser.parse_args()
    import_from_file(args.file)