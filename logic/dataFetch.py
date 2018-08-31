from database.dbSetup import dbController 
from dataFetching.dataLoader import async_fetch_all_data
from errors.errors import FetchError
from machineLearning.logic import append_estimation, append_saliency
import asyncUtils

def fetch_data_by_identifier(identifier: dict):
    """Loads resource from database from database, or if not found, 
    initiates to fetching it from external api in separate thread"""
    data = dbController.get_one(identifier)
    if data == None:
        dbController.save(identifier)
        asyncUtils.run_in_thread(_load_process_and_save, identifier)
        return None
    return data 

async def _load_process_and_save(identifier):
    """Loads, processes and saves data from external api"""
    try:
        data = await async_fetch_all_data(identifier)
        print(f":: Successfully fetched data for: {identifier}")
        # data = append_estimation(data)
        # print(f":: Successfully estimated data for: {identifier}")
        # data = append_saliency(data)
        # print(f":: Successfully added saliency data for: {identifier}")
        dbController.update(identifier, data)
    except FetchError as fetchError:
        print(f"Error occurred while fetching: {fetchError}")
        dbController.mark_as_error(identifier, fetchError)
    except Exception as exception:
        print(f"Unknown error occurred while fetching: {exception}")
        dbController.mark_as_error(identifier, exception)
        raise exception
    