import database.databaseController as db
from logic.runContainer import RunContainer

def getMatrixFromDB(identifier: dict, params: dict):
    return db.dbController.get_matrix(identifier, params)

def updateUserScore(identifier: dict, params: dict, layers):
    return db.dbController.update_user_score(identifier, params, layers)

def delete(identifier: dict):
    return db.dbController.delete(identifier)
