from pymongo import MongoClient, collection, operations

class MongoCollectionWrapper:
    def __init__(self,collection: collection.Collection):
        self.collection = collection

    def save(self, record):  
        self.collection.insert_one(record)
    
    def update(self, filter, record):  
        self.collection.replace_one(filter, record)

    def saveAll(self,recordsIterator):  
        self.collection.insert_many(recordsIterator)
    
    def getAll(self):
        return self.collection.find({})
    
    def find(self, filter, projection=None):
        return self.collection.find(filter,projection)
    
    def deleteAll(self):
        self.collection.delete_many({})

    def findOne(self, filter = {}):
        return self.collection.find_one(filter=filter)
    
    def count(self, filter={}):
        return self.collection.count_documents(filter)

    def createIndex(self, indexField, indexName, unique = "False"):
        return self.collection.create_index(indexField, name=indexName, unique=unique)

    def dropIndex(self, indexName):
        self.collection.drop_index(indexName)

    def dropIndexes(self):
        self.collection.drop_indexes()

    def dropCollection(self):
        self.collection.drop()

# class MongoFilter():
#     "$eq"	#Matches values that are equal to a specified value.
#     "$gt"	#Matches values that are greater than a specified value.
#     "$gte" 	#Matches values that are greater than or equal to a specified value.
#     "$in"	#Matches any of the values specified in an array.
#     "$lt"	#Matches values that are less than a specified value.
#     "$lte" 	#Matches values that are less than or equal to a specified value.
#     "$ne"	#Matches all values that are not equal to a specified value.
#     "$nin" 	#Matches none of the values specified in an array.

class MongoDbFactory():
    def __init__(self, dbName, client = MongoClient()):
        self.client = client
        self.db = client[dbName]

    def getCollection(self, collectionName: str):
        return self.db[collectionName]

    def getMongoCollectionWrapper(self, collectionName) -> MongoCollectionWrapper:
        collection = self.getCollection(collectionName)
        return MongoCollectionWrapper(collection)

