from database.databaseController import dbController 
from dataLoading.dataLoader import asyncFetchAllRunData
import asyncUtils

def getRunData(runNumber):
    runData = dbController.getRun(runNumber) 
    if runData == None:
        dbController.save(runNumber)
        asyncUtils.run_in_thread(loadDataAndSave, runNumber)
        return None
    return runData 

async def loadDataAndSave(run):
    data = await asyncFetchAllRunData(run)
    dbController.update(run, data)
    return data

def getFetchedRuns():
    return dbController.getFetchRunNumbers()