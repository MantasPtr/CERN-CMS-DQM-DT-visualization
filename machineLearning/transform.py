import numpy as np
from skimage.transform import resize
from functools import partial
from sklearn.preprocessing import MaxAbsScaler

SCALER = MaxAbsScaler
MATRIX_DIM = 47

def resizeMatrix(matrix):
    return list(map(resizeLayer,matrix))

def resizeLayer(layer):
    """Resizes occupancy to a given size using bilinear interpolation"""
    return resize(np.array(layer).reshape(1, len(layer)), (1, MATRIX_DIM), preserve_range=True, mode='constant', anti_aliasing=False)[0]

def scaleMatrix(matrix):
    return list(map(scaleLayer, matrix))

def scaleLayer(layer):
    layer = layer.reshape(-1, 1)
    layer = SCALER.fit(layer).transform(layer)
    return layer.reshape(1, -1)[0]

def processMatrix(matrix):
    matrix = resizeMatrix(matrix)
    matrix = scaleMatrix(matrix)
    return matrix