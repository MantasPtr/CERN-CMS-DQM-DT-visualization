import database.databaseController as db
from logic.runContainer import RunContainer

def getMatrixFromDB(runContainer: RunContainer):
    return db.dbController.getMatrix(runContainer)

def updateUserScore(runContainer: RunContainer, layers):
    return db.dbController.updateUserScore(runContainer, layers)

def deleteRun(runNumber):
    return db.dbController.deleteRun(runNumber)