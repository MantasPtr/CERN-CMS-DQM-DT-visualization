from keras.models import load_model
import numpy as np
models_directory = "./machineLearning"

snn_model = load_model("%s/cnn.h5" % models_directory)

def predict(matrix):
    return snn_model.predict(np.array(matrix))[:, 1]
