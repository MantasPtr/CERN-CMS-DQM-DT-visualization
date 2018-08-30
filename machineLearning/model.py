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

import time 
def _predict_badness(matrix) -> list:
    badLayers = list(map(_predict_layers_badness, matrix))        
    return badLayers

def _predict_layers_badness(layer) -> np.ndarray:
    if len(layer) == 0:
        return -1
    layer_result_list = cnn_model.predict(np.array([layer]))[:, 1]
    return layer_result_list[0].item()

def get_network_score(matrix) -> list:
    global graph
    with graph.as_default():
        matrix = transform.processMatrix(matrix, MATRIX_DIM)
        return _predict_badness(matrix)

def get_saliency_map(matrix) -> list:
    global graph
    with graph.as_default():
        np_matrix = np.array(matrix)
        processedMatrix = transform.processMatrix(matrix, MATRIX_DIM)
        gradients = vanilla.get_gradients(processedMatrix)
        positive_matrix = transform.remove_negatives(matrix) 
        gradients = transform.resize_matrix_to_form(gradients, positive_matrix)
        gradients = np.concatenate( gradients, axis=0 )
        filled_array = np_matrix.astype(float)
        np.place(filled_array, np_matrix != -1, gradients.reshape(-1))
        filled_array = [np_array.tolist() for np_array in filled_array]
        return filled_array
