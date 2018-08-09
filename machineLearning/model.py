from keras.models import load_model
import numpy as np
import machineLearning.transform as transform
import tensorflow as tf
MODELS_DIRECTORY = "./machineLearning"
MODEL_FILE = "cnn.h5"

cnn_model = load_model("%s/%s" % (MODELS_DIRECTORY, MODEL_FILE))
graph = tf.get_default_graph()

def predict(matrix) -> np.ndarray:
    return cnn_model.predict(np.array(matrix))[:, 1]

def getScoreForMatrix(matrix) -> np.ndarray:
    global graph
    with graph.as_default():
        matrix = transform.processMatrix(matrix)
        return predict(matrix)
