from keras.models import load_model
import numpy as np
import machineLearning.transform as transform
MODELS_DIRECTORY = "./machineLearning"
MODEL_FILE = "cnn.h5"

class Model():

    def __init__(self):
        self.cnn_model = load_model("%s/%s" % (MODELS_DIRECTORY, MODEL_FILE))
        
    def predict(self,matrix) -> np.ndarray:
        return self.cnn_model.predict(np.array(matrix))[:, 1]

    def getScoreForMatrix(self, matrix) -> np.ndarray:
        matrix = transform.processMatrix(matrix)
        return self.predict(matrix)
