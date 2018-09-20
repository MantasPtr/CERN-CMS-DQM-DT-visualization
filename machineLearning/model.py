from keras.models import load_model
import numpy as np
import machineLearning.transform as transform
import tensorflow as tf
from machineLearning.saliency import GradientSaliency
MODELS_DIRECTORY = "./machineLearning"
MODEL_FILE = "cnn.h5"
MATRIX_DIM = 47

cnn_model = load_model("%s/%s" % (MODELS_DIRECTORY, MODEL_FILE))
graph = tf.get_default_graph()
saliency_calculation = GradientSaliency(cnn_model)

def get_network_score(matrix) -> list:
    global graph
    with graph.as_default():
        matrix = transform.process_matrix(matrix, MATRIX_DIM)
        return _predict_badness(matrix)

def get_saliency_map(matrix) -> list:
    global graph
    with graph.as_default():
        processed_matrix = transform.process_matrix(matrix, MATRIX_DIM)
        gradients = np.array(saliency_calculation.get_gradients(processed_matrix))
        _replace_negatives(gradients)
        filled_matrix = transform.replace_positive_values(matrix, gradients)
        return filled_matrix

def get_saliency_map_steps(matrix) -> list:
    global graph
    with graph.as_default():
        processed_matrix = transform.process_matrix(matrix, MATRIX_DIM)
        gradients = np.array(saliency_calculation.get_gradients(processed_matrix))
        _replace_negatives(gradients)
        filled_matrix = transform.replace_positive_values(matrix, gradients)
        return filled_matrix
        return [
            {"1. matrix": matrix },
            {"2. processed matrix":processed_matrix},
            {"3. gradients": gradients},
            {"4. filled matrix:": filled_matrix},
        ]

def _replace_negatives(matrix, value = 0):
    for line in matrix:
        if len(line) != 0:
            line[line<0] = 0


def _predict_badness(matrix) -> list:
    badLayers = list(map(_predict_layers_badness, matrix))        
    return badLayers

def _predict_layers_badness(layer) -> np.ndarray:
    if len(layer) == 0:
        return -1
    layer_result_list = cnn_model.predict(np.array([layer]))[:, 1]
    return layer_result_list[0].item()