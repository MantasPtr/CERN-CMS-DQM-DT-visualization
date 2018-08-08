import machineLearning.eval as eval
import machineLearning.transform as transform

def getScoreForMatrix(matrix):
    matrix = transform.processMatrix(matrix)
    return eval.predict(matrix)

def getScoreForData(data):
    for unit in data:
        print(unit["matrix"])
        unit["scores"] = getScoreForMatrix(unit["matrix"]).tolist()
    return data
