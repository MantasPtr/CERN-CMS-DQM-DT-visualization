from config.configUtils import getConfig
from mongoWrapper import MongoDbFactory, MongoCollectionWrapper

client = None
database = None
DB_CONFIG_LOCATION='saving/mongodb.config.ini'

def getDatabaseAndCollectionName():
    config = getConfig(configLocation=DB_CONFIG_LOCATION)
    databaseName = config['database']
    collectionName = config['collection']
    return databaseName, collectionName

