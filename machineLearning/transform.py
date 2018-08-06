import numpy as np
from skimage.transform import resize
from functools import partial


def resize_occupancy(layer, min):
    """Resizes occupancy to a given size using bilinear interpolation"""
    return resize(np.array(layer).reshape(1, len(layer)), (1, min), preserve_range=True, mode='constant', anti_aliasing=False)[0]

def processMatrix(matrix):
    minimum =  min(map(len, matrix), default=0)
    resizeFunc = partial(resize_occupancy, min=minimum)
    newlayers = list(map(resizeFunc,matrix))
    return newlayers
