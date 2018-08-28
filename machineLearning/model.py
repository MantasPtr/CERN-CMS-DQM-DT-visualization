from keras.models import load_model
import numpy as np
import machineLearning.transform as transform
import tensorflow as tf
from machineLearning.saliency import GradientSaliency
import time
MODELS_DIRECTORY = "./machineLearning"
MODEL_FILE = "cnn.h5"
MATRIX_DIM = 47

cnn_model = load_model("%s/%s" % (MODELS_DIRECTORY, MODEL_FILE))
graph = tf.get_default_graph()
vanilla = GradientSaliency(cnn_model)

def _predict_badness(matrix) -> np.ndarray:
    return cnn_model.predict(np.array(matrix))[:, 1]

def get_network_score(matrix) -> np.ndarray:
    global graph
    with graph.as_default():
        matrix = transform.processMatrix(matrix, MATRIX_DIM)
        return _predict_badness(matrix)

def get_saliency_map(matrix) -> list:
    global graph
    with graph.as_default():
        processedMatrix = transform.processMatrix(matrix, MATRIX_DIM)
        mask = vanilla.get_mask(processedMatrix)
        mask = transform.resizeMatrix(mask, len(matrix[0]))
        mask = [np_array.tolist() for np_array in mask]
        return mask
