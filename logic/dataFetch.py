from database.databaseController import DbController
from dataLoading.dataLoader import fetchAllRunDataAsync
import concurrent 
import asyncUtils

dbController = DbController()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

def getRunData(runNumber):
    runData = dbController.getRun(runNumber) 
    if runData == None:
        dbController.save(runNumber)
        asyncUtils.run_in_thread(loadDataAndSave, runNumber)
        return None
    return runData 

async def loadDataAndSave(run):
    print("|||||||||||||||||||||||||||||||||||")
    data = await fetchAllRunDataAsync(run)
    print("|||||||||||||||||||||||||||||||||||")
    dbController.update(run, data)
    print("|||||||||||||||||||||||||||||||||||")
    return data

def getFetchedRuns():
    return dbController.getFetchRunNumbers()