import datetime
import time
import pymongo

class Mongo_4_DB_controller():
    def __init__(self, collection):
        self.dbCollection = collection
        self.timeOffset = datetime.datetime.now() - datetime.datetime.utcnow()

    def save(self, identifier: dict, matrix = None):
        record = self.__build_DT_record__(identifier, matrix, "LOADING")
        self.dbCollection.save(record)

    def update(self, identifier: dict, matrix):
        record = self.__build_DT_record__(identifier, matrix, "FINISHED")
        self.__assure_update__(identifier, record)

    def markAsError(self, identifier: dict, exception):
        record = self.__build_DT_record__(identifier, None, "ERROR")
        record["exception"] = str(exception)
        self.__assure_update__(identifier, record)

    def __assure_update__(self, *args):
        rez = self.dbCollection.update(*args)
        if rez["nModified"] == 0:
            print(f"WARNING: update with criteria:{args[0]} did not update any records!")

    def getOne(self, identifier: dict):
        return self.dbCollection.find_one(identifier)

    def getMatrix(self, identifier: dict, paramsDict: dict):
        cursor = self.dbCollection.aggregate([
            {
                "$match":{ "identifier": identifier}
            },
            {
                "$project":{ 
                    "identifier":1,
                    "data": {
                        "$filter":{ 
                            "input":"$data", 
                            "as":"item", 
                            "cond":{ 
                                "$and": [{"$eq": criteria for criteria in self.__buildParamObjectFilter__("$$item.params.", paramsDict)}]
                            }
                        }
                    } 
                }
            }
        ])
        if not cursor.alive:
            return None
        return cursor.next()

    def __buildParamObjectFilter__(self, prename: str, paramsDict: dict ):
        return [(prename + key,value) for key, value in paramsDict.items()]

    def getAllFetchedData(self):
        data = self.dbCollection.find({}, {"identifier": 1, "status": 1, "save_time": 1, "data":1, "exception": 1}).sort("save_time", pymongo.DESCENDING)
        return list(map(self.__formatFetchedData__, data))

    def __formatFetchedData__(self, record: dict):
        datatime = record["save_time"] + self.timeOffset
        record.pop("_id")
        record["save_time"]= "%d-%02d-%02d %02d:%02d:%02d" % (datatime.year, datatime.month, datatime.day, datatime.hour, datatime.minute, datatime.second)
        return record

    def __build_DT_record__(self, identier: dict, matrix, status):
        return {
            "identifier": identier,
            "status": status,
            "save_time": datetime.datetime.utcnow(),
            "data": matrix
        }

    def updateUserScore(self, identifierDict: dict, paramDict: dict, badLayers: list):
        paramFilter = dict(self.__buildParamObjectFilter__("data.params.",paramDict))
        paramFilter.update({"identifier":identifierDict})
        rez = self.dbCollection.update(paramFilter
            ,{
                "$set" : { "data.$.user_scores":badLayers }
            })
        return {"matched":rez["n"], "updated": rez["nModified"] == 0 }

    def delete(self, identifier: dict):
        print(identifier)
        rez = self.dbCollection.delete_one({"identifier": identifier})
        return rez.deleted_count