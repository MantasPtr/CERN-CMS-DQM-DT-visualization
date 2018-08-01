import datetime
import time

class Mongo_4_DB_controller():
    def __init__(self, collection):
        self.runsCollection = collection
        self.timeOffset = datetime.datetime.now() - datetime.datetime.utcnow()
        # TODO: create indexes only is not exist 
        # unique_indexes = config["uniqueIndex"].split(",")
        # for indexFieldName in unique_indexes:
        #     self.runData.createIndex(indexFieldName, indexFieldName + "_index", True)

    def save(self, run, matrix = None):
        record = self.__build_DT_record__(run, matrix, "LOADING")
        self.runsCollection.save(record)

    def update(self, run, matrix):
        record = self.__build_DT_record__(run, matrix, "FINISHED")
        self.runsCollection.update({"run" : run}, record)

    def markAsError(self, run, exception):
        record = self.__build_DT_record__(run, None, "ERROR")
        record["exception"] = str(exception)
        self.runsCollection.update({"run" : run}, record)

    def __build_DT_record__(self, run, matrix, status):
        return {
            "run": run,
            "status": status,
            "save_time": datetime.datetime.utcnow(),
            "data": matrix
        }

    def getRun(self, run):
        return self.runsCollection.find_one({"run": run})

    def getMatrix(self, run, wheel, sector, station):
        return self.runsCollection.aggregate([
            {
                "$match":{ "run": run }
            },
            {
                "$project":{ 
                    "run":1,
                    "data": {
                        "$filter":{ 
                            "input":"$data", 
                            "as":"item", 
                            "cond":{ 
                                "$and": [
                                    {"$eq": ["$$item.params.wheel",   wheel]},
                                    {"$eq": ["$$item.params.sector",  sector]},
                                    {"$eq": ["$$item.params.station", station]} 
                                ]
                            }
                        }
                    } 
                }
            }
        ]).next()
    
    def getFetchRunNumbers(self):
        runs = self.runsCollection.find({}, {"run": 1, "status": 1, "save_time": 1, "exception": 1})
        return map(self.__formatFetchedRunData__, runs)

    def __formatFetchedRunData__(self, run: dict):
        datatime = run["save_time"] + self.timeOffset
        run.pop("_id")
        run["save_time"]= "%d-%02d-%02d %02d:%02d:%02d" % (datatime.year, datatime.month, datatime.day, datatime.hour, datatime.minute, datatime.second)
        return run