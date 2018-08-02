import database.databaseController as db
from logic.runContainer import RunContainer

def getMatrixFromDB(run :RunContainer):
    return db.dbController.getMatrix(run)

def updateUserScores(run, wheel, sector, station):
    return None