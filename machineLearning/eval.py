from keras.models import load_model
import numpy as np
models_directory = "./machineLearning"


def loadModel():
    global cnn_model
    cnn_model = load_model("%s/cnn.h5" % models_directory)

def predict(matrix):
    global cnn_model
    if cnn_model is None:
        loadModel()
    return cnn_model.predict(np.array(matrix))[:, 1]

cnn_model = None