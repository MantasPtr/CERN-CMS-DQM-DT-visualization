from config.configUtils import getConfig

client = None
database = None
DB_CONFIG_LOCATION='saving/mongodb.config.ini'

def getDatabaseAndCollectionName():
    config = getConfig(configLocation=DB_CONFIG_LOCATION)
    databaseName = config['database']
    collectionName = config['collection']
    return {"database":databaseName, "collection":collectionName}