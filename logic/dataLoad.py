from database.dbSetup import dbController

def getMatrixFromDB(identifier: dict, params: dict):
    return dbController.get_matrix(identifier, params)

def updateUserScore(identifier: dict, params: dict, layers: list):
    return dbController.update_user_score(identifier, params, layers)

def delete(identifier: dict):
    return dbController.delete(identifier)

def getFetchedData():
    return dbController.get_all()

def getScoresData():
    return dbController.get_all_user_scores()

def get_network_scores():
    return dbController.get_all_network_scores()