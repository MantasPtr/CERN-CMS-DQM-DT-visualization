from database.dbSetup import dbController 
from dataLoading.dataLoader import asyncFetchAllData
from errors.errors import FetchError
import asyncUtils

def getDataByIdentifier(identifier: dict):
    data = dbController.get_one(identifier)
    if data == None:
        dbController.save(identifier)
        asyncUtils.run_in_thread(load_data_and_save, identifier)
        return None
    return data 

async def load_data_and_save(identifier):
    try:
        data = await asyncFetchAllData(identifier)
        print(f":: Successfully fetch data for: {identifier}")
        dbController.update(identifier, data)
    except FetchError as fetchError:
        print(f"Known error occurred while fetching: {fetchError}")
        dbController.mark_as_error(identifier, fetchError)
    except Exception as exception:
        print(f"Unknown error occurred while fetching: {exception}")
        dbController.mark_as_error(identifier, exception)
        raise exception
