import csv

def read_file(file_name: str) -> iter:
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        for record in reader:
            yield record