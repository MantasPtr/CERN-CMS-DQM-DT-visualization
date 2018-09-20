import numpy as np

def to_python_matrix(data):
    if type(data) is np.ndarray:
        data = data.tolist()
    if type(data) is list:
        data = [to_python_matrix(x) for x in data] 
    return data

def remove_negatives(data: list) -> list:
    return [x for x in data if x >= 0]