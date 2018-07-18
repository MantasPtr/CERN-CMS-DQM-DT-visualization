from pymongo import MongoClient, collection

class MongoCollectionWrapper:
    def __init__(self,collection: collection.Collection):
        self.collection = collection

    def save(self,record):  
        self.collection.insert_one(record)
    
    def saveAll(self,recordsIterator):  
        self.collection.insert_many(recordsIterator)
    
    def getAll(self):
        return self.collection.find({})
    
    def find(self, filter):
        return self.collection.find(filter)
    
    def deleteAll(self):
        self.collection.delete_many({})

    def findOne(self, filter = {}):
        return self.collection.find_one(filter)

    def count(self, filter={}):
        return self.collection.count_documents(filter)


class MongoDbFactory():
    def __init__(self, dbName, client = MongoClient()):
        self.client = client
        self.db = client[dbName]

    def getCollection(self, collectionName: str):
        return self.db[collectionName]

    def getMongoCollectionWrapper(self, collectionName) -> MongoCollectionWrapper:
        collection = self.getCollection(collectionName)
        return MongoCollectionWrapper(collection)

