import datetime
import time
import pymongo
import warnings
from typing import Tuple, List

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
        # {'identifier': {'xy': 123},"data": {$elemMatch: { "params.x_key": x_value, "params.y_key:y_value}}},{"$set": {"data.$.user_scores": [1,2,3]}} 
        return self._assure_update(
            {   
                "identifier": identifier, 
                "data": {"$elemMatch": { ("params."+str(key)):value for key,value in paramDict.items() }}
            },{
                "$set": {"data.$.user_scores":badLayers}
            }
            )

    def delete(self, identifier: dict):
        print(identifier)
        rez = self.dbCollection.delete_one({"identifier": identifier})
        return rez.deleted_count

    def get_one(self, identifier: dict):
        return self.dbCollection.find_one({"identifier": identifier})

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
                                # "$and": [
                                #       {"$eq": ["$$item.params.x_key", x_value]}
                                #       {"$eq": ["$$item.params.y_key", y_value]}
                                #   ]
                                "$and": [{"$eq": [("$$item.params." + str(key)), value] for key, value in paramsDict.items()}]
                            }
                        }
                    } 
                }
            }
        ])
        return cursor.next()

    def get_all_user_scores(self):
        cursor = self.dbCollection.aggregate([
        #     {"$unwind": "$data" },
        #     {"$match": {"data.user_scores": {"$exists": True}} },
        #     {"$group": {"_id":"$identifier", "params":{"$push": "$data.params"}, "user_scores":{"$push":'$data.user_scores'}} },
        #     {"$project": {"_id":0, "identifier":"$_id", "user_scores":1, "params":1} } 
        # ])
            {"$unwind": "$data" },
            {"$match": {"data.user_scores": {"$exists": True}} },
            {"$project": {"_id":0, "identifier":1, "data.user_scores":1, "data.params":1} } 
        ])
        return list(cursor)

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

   

    