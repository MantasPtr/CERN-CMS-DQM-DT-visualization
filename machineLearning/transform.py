import numpy as np
from skimage.transform import resize
from functools import partial
from sklearn.preprocessing import MaxAbsScaler

SCALER = MaxAbsScaler

def resizeMatrix(matrix):
    minimum =  min(map(len, matrix), default=0)
    resizeFunc = partial(resizeLayer, requiredSize=minimum)
    return list(map(resizeFunc,matrix))

def resizeLayer(layer, requiredSize):
    """Resizes occupancy to a given size using bilinear interpolation"""
    return resize(np.array(layer).reshape(1, len(layer)), (1, requiredSize), preserve_range=True, mode='constant', anti_aliasing=False)[0]

def scaleMatrix(matrix):
    return list(map(scaleLayer, matrix))

def scaleLayer(layer):
    layer = layer.reshape(-1, 1)
    layer = SCALER.fit_transform(layer)
    return layer.reshape(1, -1)

def processMatrix(matrix):
    matrix = resizeMatrix(matrix)
    matrix = scaleMatrix(matrix)
    return matrix