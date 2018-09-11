import numpy as np
from skimage.transform import resize
from functools import partial
from sklearn.preprocessing import MaxAbsScaler

SCALER = MaxAbsScaler

def resizeMatrix(matrix, model_dim):
    return [resizeLayer(line, model_dim) for line in matrix]

def resizeLayer(layer: list, model_dim) -> np.ndarray:
    """Resizes line to a given size using bilinear interpolation"""
    if len(layer) == 0 or model_dim == 0:
        return np.array([])
    return resize(np.array(layer).reshape(1, len(layer)), (1, model_dim), preserve_range=True, mode='constant', anti_aliasing=False)[0]

def resize_matrix_to_form(matrix, form) -> np.ndarray:
    """Resizes each layer of matrix to a given matrix layer size using bilinear interpolation"""
    return [resizeLayer(line, len(form[index])) for index,line in enumerate(matrix)]

def scaleMatrix(matrix):
    return list(map(scaleLayer, matrix))

def scaleLayer(layer: np.ndarray) -> np.ndarray : 
    if len(layer) == 0:
        return layer
    layer = np.array(layer)
    layer = layer.reshape(-1, 1)
    layer = SCALER().fit(layer).transform(layer)
    return layer.reshape(1, -1)[0]

def remove_negatives(matrix):
    positive =  [[x for x in line if x >= 0 ] for line in matrix]
    return positive

def process_matrix(matrix, model_dim):
    matrix = remove_negatives(matrix)
    matrix = resizeMatrix(matrix, model_dim)
    matrix = scaleMatrix(matrix)
    return matrix

def replace_positive_values(matrix_to_fill, filler):
    np_matrix = np.array(matrix_to_fill)
    positive_matrix = remove_negatives(matrix_to_fill) 
    filler = resize_matrix_to_form(filler, positive_matrix)
    filler = np.concatenate(filler, axis=0 )
    filled_array = np_matrix.astype(float)
    np.place(filled_array, np_matrix >= 0, filler.reshape(-1))
    filled_array = [np_array.tolist() for np_array in filled_array]
    return filled_array