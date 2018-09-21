from database.dbSetup import get_db_controller 
from dataFetching.dataLoader import async_fetch_all_data
from errors.errors import FetchError
import logic.dataEvaluation as dataEvaluation
from utils import asyncUtils
import asyncio

def fetch_data_by_identifier(identifier: dict):
    """Loads resource from database from database, or if not found, 
    initiates to fetching it from external api in separate thread"""
    data = get_db_controller().get_one(identifier) # TODO: replace with less db intensive check like count
    if data == None:
        get_db_controller().save(identifier, status = "LOADING")
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
        get_db_controller().update(identifier, data = data, status = "FINISHED")
    except FetchError as fetchError:
        print(f"Error occurred while fetching: {fetchError}")
        get_db_controller().update(identifier, status = "ERROR", other = {"exception": str(fetchError)})
    except Exception as exception:
        print(f"Unknown error occurred while fetching: {exception}")
        get_db_controller().update(identifier, status = "ERROR", other = {"exception": str(exception)})
        raise exception

def reevaluate_all():
   asyncUtils.run_async_in_thread(reevaluate_all_async)

def _reevaluate_all():
    try:
        data = get_db_controller().get_all()
        for record in data:
            identifier = record.get("identifier")
            get_db_controller().update_status(identifier, status = "REEVALUATING")
            data = dataEvaluation.process(record["data"])
            print(f":: Successfully reevaluated  data for: {identifier}")
            get_db_controller().update(identifier, data = data, status = "FINISHED")
    except Exception as exception:
        print(f"Unknown error occurred while fetching: {exception}")
        get_db_controller().update_status(identifier, status = "ERROR", other = {"exception": str(exception)})
        raise exception

async def reevaluate_all_async():
    data = get_db_controller().get_all()
    downloaded_data = [x for x in data if x["status"] in ["REEVALUATING", "FINISHED", "PENDING_REEVALUATION"]]
    for record in downloaded_data:
        identifier = record.get("identifier")
        get_db_controller().update_status(identifier, status = "PENDING_REEVALUATION")
    await asyncio.gather(*[reevaluate(d) for d in downloaded_data])

async def reevaluate(record):
    try:
        identifier = record.get("identifier")
        get_db_controller().update_status(identifier, status = "REEVALUATING")
        data = dataEvaluation.process(record["data"])
        get_db_controller().update(identifier, data = data, status = "FINISHED")
        print(f":: Successfully reevaluated  data for: {identifier}")
    except Exception as exception:
        print(f"Unknown error occurred while reevalutating record {identifier}: error: {exception}")
        get_db_controller().update_status(identifier, status = "ERROR", other = {"exception": str(exception)})
        raise exception

def visualize(identifier: dict, params: dict):
    record = get_db_controller().get_single_record_matrix(identifier, params)
    return dataEvaluation.visualize_saliency(record)