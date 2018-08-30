from config.configUtils import getConfig
from database.mongoController import Mongo_4_DB_controller
from database.mongoDbFactory import MongoDbFactory

DB_CONFIG_LOCATION='database/config/mongodb.config.ini'

def init_database() -> Mongo_4_DB_controller:
    db, col = get_default_database_config()
    collection = MongoDbFactory(db).getCollection(col)
    return Mongo_4_DB_controller(collection)

def get_default_database_config():
    config = getConfig(DB_CONFIG_LOCATION)
    database = config["database"]
    collection = config["collection"]
    return database, collection

dbController = init_database()