from database.dbSetup import getDatabaseConfig
from database.mongoWrapper import MongoDbFactory, MongoCollectionWrapper
import datetime

class DbController():
    def __init__(self):
        config = getDatabaseConfig()
        db = config["database"]
        col = config["collection"]
        self.runData: MongoCollectionWrapper = MongoDbFactory(db).getMongoCollectionWrapper(col)

        # TODO: create indexes only is not exist 
        # unique_indexes = config["uniqueIndex"].split(",")
        # for indexFieldName in unique_indexes:
        #     self.runData.createIndex(indexFieldName, indexFieldName + "_index", True)

    def save(self, run, matrix = None):
        record = self.__build_DT_record__(run, matrix, "LOADING")
        self.__save_DT_record__(record)

    def update(self, run, matrix):
        record = self.__build_DT_record__(run, matrix, "FINISHED")
        self.__update_DT_record__({"run" : run}, record)

    def markAsError(self, run):
        record = self.__build_DT_record__(run, None, "ERROR")
        self.__update_DT_record__({"run" : run}, record)

    def __build_DT_record__(self, run, matrix, status):
        return {
            "run": run,
            "status": status,
            "save_time": datetime.datetime.utcnow(),
            "data": matrix
        }

    def __update_DT_record__(self, filter, record):
        self.runData.update(filter, record)

    def __save_DT_record__(self, record):
        self.runData.save(record)

    def getRun(self, run):
        return self.runData.findOne({"run": run})

    def getFetchRunNumbers(self):
        runs = self.runData.find({}, {"run": 1, "status": 1, "save_time": 1})
        return map(self.__formatFetchedRunData, runs)

    def __formatFetchedRunData(self, run: dict):
        datatime = run["save_time"]
        run.pop("_id")
        run["save_time"]= "%d-%02d-%02d %02d:%02d:%02d" % (datatime.year, datatime.month, datatime.day, datatime.hour, datatime.minute, datatime.second)
        return run

dbController = DbController()

