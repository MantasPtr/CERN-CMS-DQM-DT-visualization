from pymongo import MongoClient, collection, operations

class MongoDbFactory():
    def __init__(self, dbName, client = MongoClient()):
        self.client = client
        self.db = client[dbName]

    def getCollection(self, collectionName: str):
        return self.db[collectionName]
         