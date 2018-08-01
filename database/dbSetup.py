from config.configUtils import getConfig
from database.mongoController import Mongo_4_DB_controller
from database.mongoDbFactory import MongoDbFactory

DB_CONFIG_LOCATION='config/mongodb.config.ini'

def getDefaultDatabaseConfig():
    config = getConfig(configLocation=DB_CONFIG_LOCATION)
    database = config["database"]
    collection = config["collection"]
    return database, collection

def initDatabase() -> Mongo_4_DB_controller:
    db, col = getDefaultDatabaseConfig()
    collection = MongoDbFactory(db).getCollection(col)
    return Mongo_4_DB_controller(collection)