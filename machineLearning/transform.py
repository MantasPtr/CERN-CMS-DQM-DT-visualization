import numpy as np
from skimage.transform import resize
from functools import partial
from sklearn.preprocessing import MaxAbsScaler

SCALER = MaxAbsScaler

def resizeMatrix(matrix, model_dim):
    return [resizeLayer(line, model_dim) for line in matrix]

def resizeLayer(layer: list, model_dim) -> np.ndarray:
    if len(layer) == 0:
        return np.array(layer)  
    """Resizes occupancy to a given size using bilinear interpolation"""
    return resize(np.array(layer).reshape(1, len(layer)), (1, model_dim), preserve_range=True, mode='constant', anti_aliasing=False)[0]

def scaleMatrix(matrix):
    return list(map(scaleLayer, matrix))

def scaleLayer(layer: np.ndarray) -> np.ndarray : 
    if len(layer) == 0:
        return layer
    layer = layer.reshape(-1, 1)
    layer = SCALER().fit(layer).transform(layer)
    return layer.reshape(1, -1)[0]

def removeNegatives(matrix):
    positive =  [[x for x in line if x >= 0 ] for line in matrix]
    return positive

def processMatrix(matrix, model_dim):
    matrix = removeNegatives(matrix)
    matrix = resizeMatrix(matrix, model_dim)
    matrix = scaleMatrix(matrix)
    return matrix