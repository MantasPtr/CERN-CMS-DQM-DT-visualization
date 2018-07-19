from saving.dbSetup import getDatabaseAndCollectionName
from saving.mongoWrapper import MongoDbFactory, MongoCollectionWrapper

class DbController():
    def __init__(self):
        db, col = getDatabaseAndCollectionName()
        self.data: MongoCollectionWrapper = MongoDbFactory(db).getMongoCollectionWrapper(col)

    def save(self, run, matrix):
        record = self.__build_DT_record(run, matrix)
        self.__save_DT_record(record)

    def __build_DT_record(self, run, matrix):
        return {
            "run": run,
            "save_time": datetime.datetime.utcnow(),
            "data": matrix
        }

    def __save_DT_record(self, record):
        self.data.save(record)
