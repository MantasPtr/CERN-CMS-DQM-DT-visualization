from database.dbSetup import dbController 
from dataFetching.dataLoader import async_fetch_all_data
from errors.errors import FetchError
import logic.dataEvaluation as dataEvaluation
from utils import asyncUtils
import asyncio

def fetch_data_by_identifier(identifier: dict):
    """Loads resource from database from database, or if not found, 
    initiates to fetching it from external api in separate thread"""
    data = dbController.get_one(identifier)
    if data == None:
        dbController.save(identifier, status = "LOADING")
        asyncUtils.run_async_in_thread(_load_process_and_save, identifier)
        return None
    return data 

async def _load_process_and_save(identifier):
    """Loads, processes and saves data from external api"""
    try:
        data = await async_fetch_all_data(identifier)
        print(f":: Successfully fetched data for: {identifier}")
        data = dataEvaluation.process(data)
        print(f":: Successfully processed data for: {identifier}")
        dbController.update(identifier, data = data, status = "FINISHED")
    except FetchError as fetchError:
        print(f"Error occurred while fetching: {fetchError}")
        dbController.update(identifier, status = "ERROR", other = {"exception": str(exception)})
    except Exception as exception:
        print(f"Unknown error occurred while fetching: {exception}")
        dbController.update(identifier, status = "ERROR", other = {"exception": str(exception)})
        raise exception

def reevaluate_all():
   asyncUtils.run_async_in_thread(reevaluate_all_async)

def _reevaluate_all():
    try:
        data = dbController.get_all()
        for record in data:
            identifier = record.get("identifier")
            dbController.update_status(identifier, status = "REEVALUATING")
            data = dataEvaluation.process(record["data"])
            print(f":: Successfully reevaluated  data for: {identifier}")
            dbController.update(identifier, data = data, status = "FINISHED")
    except Exception as exception:
        print(f"Unknown error occurred while fetching: {exception}")
        dbController.update_status(identifier, status = "ERROR", other = {"exception": str(exception)})
        raise exception

async def reevaluate_all_async():
    data = dbController.get_all()
    for record in data:
        identifier = record.get("identifier")
        dbController.update_status(identifier, status = "PENDING_REEVALUATION")
    await asyncio.gather(*[reevaluate(d) for d in data])

async def reevaluate(record):
    identifier = record.get("identifier")
    dbController.update_status(identifier, status = "REEVALUATING")
    data = dataEvaluation.process(record["data"])
    print(f":: Successfully reevaluated  data for: {identifier}")
    dbController.update(identifier, data = data, status = "FINISHED")

def visualize(identifier: dict, params: dict):
    record = dbController.get_single_record_matrix(identifier, params)
    return dataEvaluation.visualize_saliency(record)