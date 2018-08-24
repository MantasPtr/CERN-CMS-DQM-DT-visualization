from keras.models import load_model
import numpy as np
import machineLearning.transform as transform
import tensorflow as tf
from machineLearning.saliency import GradientSaliency
MODELS_DIRECTORY = "./machineLearning"
MODEL_FILE = "cnn.h5"

cnn_model = load_model("%s/%s" % (MODELS_DIRECTORY, MODEL_FILE))
graph = tf.get_default_graph()

def _predict(matrix) -> np.ndarray:
    return cnn_model.predict(np.array(matrix))[:, 1]

def get_network_score(matrix) -> np.ndarray:
    global graph
    with graph.as_default():
        matrix = transform.processMatrix(matrix)
        return _predict(matrix)

def get_saliency_map(matrix) -> np.ndarray:
    # global graph
    # with graph.as_default():
    #     matrix = transform.processMatrix(matrix)
    #     return predict(matrix)
    vanilla = GradientSaliency(cnn_model)
    matrix = transform.processMatrix(matrix)
    mask = vanilla.get_mask(matrix)
    return mask

