import database.databaseController

def getMatrixFromDB(run, wheel, sector, station):
    return database.databaseController.dbController.getMatrix(run, wheel, sector, station)