from config.configUtils import getConfig
from database.mongoWrapper import MongoDbFactory, MongoCollectionWrapper

client = None
database = None
DB_CONFIG_LOCATION='config/mongodb.config.ini'

def getDatabaseConfig():
    return getConfig(configLocation=DB_CONFIG_LOCATION)
