import csv
import os

def write_to_file(file_name: str, data: iter, directory: str = None):
    if directory:
        _ensure_directory(directory)
        file_name = f"{directory}/{file_name}" 
    with open(file_name, 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)

def _ensure_directory(path: str):
    os.makedirs(path, exist_ok=True)