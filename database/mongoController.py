import datetime
import time
import pymongo
import warnings

class Mongo_4_DB_controller():
    def __init__(self, collection):
        self.dbCollection = collection
        self.timeOffset = datetime.datetime.now() - datetime.datetime.utcnow()

    def save(self, identifier: dict, matrix = None):
        record = self._build_db_record(identifier, matrix, "LOADING")
        self.dbCollection.save(record)

    def update(self, identifier: dict, matrix):
        record = self._build_db_record(identifier, matrix, "FINISHED")
        self._assure_update({"identifier": identifier}, record)

    def mark_as_error(self, identifier: dict, exception):
        record = self._build_db_record(identifier, None, "ERROR")
        record["exception"] = str(exception)
        self._assure_update(identifier, record)

    def update_user_score(self, identifier: dict, paramDict: dict, badLayers: list):
        paramFilter = self._build_filter_with_identifier("data.params.", paramDict, identifier)
        return self._assure_update(paramFilter, {"$set" : {"data.$.user_scores":badLayers} })

    def delete(self, identifier: dict):
        print(identifier)
        rez = self.dbCollection.delete_one({"identifier": identifier})
        return rez.deleted_count

    def get_one(self, identifier: dict):
        return self.dbCollection.find_one(identifier)

    def get_all(self):
        data = self.dbCollection.find({}, {"identifier": 1, "status": 1, "save_time": 1, "data":1, "exception": 1}).sort("save_time", pymongo.DESCENDING)
        return list(map(self._format_db_result, data))


    def get_matrix(self, identifier: dict, paramsDict: dict):
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
                                "$and": [{"$eq": criteria for criteria in self._build_param_filter("$$item.params.", paramsDict)}]
                            }
                        }
                    } 
                }
            }
        ])
        if not cursor.alive:
            return None
        return cursor.next()

    def _assure_update(self, *args):
        rez = self.dbCollection.update(*args)
        if rez["nModified"] == 0:
            warnings.warn(f"Update with criteria:{args[0]} did not update any records!")
        return {"matched":rez["n"], "updated": rez["nModified"] == 0 }

    def _format_db_result(self, record: dict):
        datatime = record["save_time"] + self.timeOffset
        record.pop("_id")
        record["save_time"]= "%d-%02d-%02d %02d:%02d:%02d" % (datatime.year, datatime.month, datatime.day, datatime.hour, datatime.minute, datatime.second)
        return record

    def _build_db_record(self, identier: dict, matrix, status):
        return {
            "identifier": identier,
            "status": status,
            "save_time": datetime.datetime.utcnow(),
            "data": matrix
        }

    def _build_param_filter(self, prename: str, paramsDict: dict ):
        return [(prename + key,value) for key, value in paramsDict.items()]

    def _build_filter_with_identifier(self, prename: str ,paramDict: dict, identifier: dict):
        paramFilter = dict(self._build_param_filter(prename ,paramDict))
        paramFilter.update({"identifier":identifier})
        return paramFilter

    # def getEvaluatedScores(self, id)

    