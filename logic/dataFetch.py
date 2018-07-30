from database.databaseController import dbController 
from dataLoading.dataLoader import asyncFetchAllRunData
from errors.errors import FetchError
import asyncUtils

def getRunData(runNumber):
    runData = dbController.getRun(runNumber) 
    if runData == None:
        dbController.save(runNumber)
        asyncUtils.run_in_thread(loadDataAndSave, runNumber)
        return None
    return runData 

async def loadDataAndSave(run):
    try:
        data = await asyncFetchAllRunData(run)
        print(f":: Successfully fetch data for run:{run}")
        dbController.update(run, data)
    except FetchError:
        dbController.markAsError(run)
    return data

def getFetchedRuns():
    return dbController.getFetchRunNumbers()