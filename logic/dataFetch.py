from database.databaseController import dbController 
from dataLoading.dataLoader import asyncFetchAllData
from errors.errors import FetchError
import asyncUtils

def getDataByIdentifier(identifier: dict):
    data = dbController.getOne(identifier)
    if data == None:
        dbController.save(identifier)
        asyncUtils.run_in_thread(loadDataAndSave, identifier)
        return None
    return data 

async def loadDataAndSave(identifier):
    try:
        data = await asyncFetchAllData(identifier)
        print(f":: Successfully fetch data for: {identifier}")
        dbController.update(identifier, data)
    except FetchError as fetchError:
        print(f"Known error occurred while fetching: {fetchError}")
        dbController.markAsError(identifier, fetchError)
    except Exception as exception:
        print(f"Unknown error occurred while fetching: {exception}")
        dbController.markAsError(identifier, exception)
        raise exception

def getFetchedData():
    return dbController.getAllFetchedData()
