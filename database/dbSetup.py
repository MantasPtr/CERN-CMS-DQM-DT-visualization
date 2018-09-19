from config.configUtils import getConfig
from database.mongoController import Mongo_4_DB_controller
from pymongo import MongoClient, collection, operations

DB_CONFIG_LOCATION='database/config/mongodb.config.ini'
_default_db_controller = None
_client = MongoClient()

def get_db_controller(database: str = None, collection: str = None)-> Mongo_4_DB_controller:
    if (database == None and  collection == None):
        global _default_db_controller
        _default_db_controller = _default_db_controller or _init_default_controller()
        return _default_db_controller
    else:
        return Mongo_4_DB_controller(_get_collection(database, collection))

def _init_default_controller() -> Mongo_4_DB_controller:
    db, col = _get_default_database_config()
    collection = _get_collection(db,col)
    return Mongo_4_DB_controller(collection)

def _get_default_database_config():
    config = getConfig(DB_CONFIG_LOCATION)
    database = config["database"]
    collection = config["collection"]
    return database, collection

def _get_collection(db_name: str, collection_name: str, client = _client):
    return client[db_name][collection_name]
