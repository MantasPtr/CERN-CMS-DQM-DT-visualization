import sys
sys.path.append("/afs/cern.ch/user/m/mpetrika/private/cms/task/")

import csvDataConverter, csvFileWriter
from datetime import datetime
from database import dbSetup as db

DIRECTORY="exported_files"
FILE_PREFIX = "dt_"

def export_to_file():
    db_records = _load_from_database()
    data = _process_data(db_records)
    file_name = _get_file_name()
    _write_to_file(file_name, data)

def _load_from_database():
    return db.dbController.get_all_user_scores()

def _process_data(db_records: iter) -> iter :
    return csvDataConverter.from_record_to_row(db_records)

def _get_file_name():
    return f"{FILE_PREFIX}{datetime.now()}.csv".replace(" ", "_")

def _write_to_file(file_name: str,  data: iter):
    print(f"Writing to file: {file_name}")
    csvFileWriter.write_to_file(file_name, data, directory=DIRECTORY)

if __name__ == '__main__':
    export_to_file()