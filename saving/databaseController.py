from saving.dbSetup import getDatabaseAndCollectionName
from saving.mongoWrapper import MongoDbFactory, MongoCollectionWrapper

class DbController():
    def __init__(self):
        db, col = getDatabaseAndCollectionName()
        self.data = MongoDbFactory(db).getMongoCollectionWrapper(col)