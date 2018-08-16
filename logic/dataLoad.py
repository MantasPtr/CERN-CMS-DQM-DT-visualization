import database.databaseController as db
from logic.runContainer import RunContainer

def getMatrixFromDB(identifier: dict, params: dict):
    return db.dbController.getMatrix(identifier, params)

def updateUserScore(identifier: dict, params: dict, layers):
    return db.dbController.updateUserScore(identifier, params, layers)

def delete(identifier: dict):
    return db.dbController.delete(identifier)
