from saving.databaseController import DbController
from dataLoading.dataLoader import fetchAllRunData

dbController = DbController()

def loadDataAndSave(run):
    data = fetchAllRunData(run)
    dbController.save(run, data)
    return data

def getFetchedRuns():
    return dbController.getFetchRunNumbers()