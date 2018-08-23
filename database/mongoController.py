import datetime
import time
import pymongo
import warnings
from errors.errors import NotSingleResultError
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
        return self._assure_update({   
                "identifier": identifier, 
                "data": {"$elemMatch": { ("params."+str(key)):value for key,value in paramDict.items() }}
            },{
                "$set": {"data.$.evaluation.bad_layers":badLayers, "data.$.evaluation.eval_time": datetime.datetime.utcnow(), "data.$.evaluation.skipped":False}
            })

    def skip_user_score(self, identifier: dict, paramDict: dict):
        return self._assure_update({   
                "identifier": identifier, 
                "data": {"$elemMatch": { ("params."+str(key)):value for key,value in paramDict.items() }}
            },{
                "$set": {"data.$.evaluation.skipped": True}
            })

    def delete(self, identifier: dict):
        print(identifier)
        rez = self.dbCollection.delete_one({"identifier": identifier})
        return rez.deleted_count

    def get_one(self, identifier: dict):
        return self.dbCollection.find_one({"identifier": identifier})

    def get_all(self):
        data = self.dbCollection.find({}, {"_id": 0 ,"identifier": 1, "status": 1, "save_time": 1, "data":1, "exception": 1}).sort("save_time", pymongo.DESCENDING)
        return list(map(self._format_db_result_datatime, data))

    def _format_db_result_datatime(self, record: dict):
        datatime = record["save_time"] + self.timeOffset
        record["save_time"]= "%d-%02d-%02d %02d:%02d:%02d" % (datatime.year, datatime.month, datatime.day, datatime.hour, datatime.minute, datatime.second)
        return record

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
                                "$and": [{"$eq": ["$$item.params." + str(key),value]} for key, value in paramsDict.items()]
                            }
                        }
                    } 
                }
            }
        ])
        return self._get_single_result(cursor)

    def get_all_user_scores(self):
        cursor = self.dbCollection.aggregate([
            {"$unwind": "$data" },
            {"$match": {"data.evaluation.bad_layers": {"$exists": True}} },
            {"$project": {"_id":0, "identifier":1, "data.evaluation":1, "data.params":1} } 
        ])
        return list(cursor)

    def get_all_network_scores(self, limit):
        cursor = self.dbCollection.aggregate( [
            {"$match": {"status":"FINISHED"}},
            {"$unwind": "$data" },
            {"$project": {
                "_id":0,
                "identifier":1,
                "data.params":1,
                "data.scores":1,
                "rating": self._get_score_eval_pipeline()
            }},
            {"$sort": {"rating":1}},
            {"$limit": limit}
        ])
        return list(cursor)

    def get_not_evaluated_network_scores(self, limit):
        cursor = self.dbCollection.aggregate( [
            {"$match": {"status":"FINISHED"}},
            {"$unwind": "$data" },
            {"$match": { "$and": [
                {"data.evaluation.skipped": {"$nin": [True]}},
                {"data.evaluation.bad_layers": {"$exists": False}}
            ]}},
            {"$project": {
                "_id":0,    
                "identifier":1,
                "data.params":1,
                "data.scores":1,
                "rating": self._get_score_eval_pipeline()
            }},
            {"$sort": {"rating":1}},
            {"$limit": limit}
        ])
        return list(cursor)

    def _get_score_eval_pipeline(self):
        return {"$reduce": {
                        "input": "$data.scores",
                        "initialValue": 0.5,
                        "in": {
                            "$min":[
                                "$$value",
                                { "$abs":  {"$subtract": [0.5, "$$this"]}}
                            ]
                        }
                    }
                }

    def _assure_update(self, *args):
        rez = self.dbCollection.update(*args)
        if rez["nModified"] == 0:
            warnings.warn(f"Update with criteria:{args[0]} did not update any records!")
        return {"matched":rez["n"], "updated": rez["nModified"] == 0 }

    def _build_db_record(self, identifier: dict, matrix, status):
        return {
            "identifier": identifier,
            "status": status,
            "save_time": datetime.datetime.utcnow(),
            "data": matrix
        }

    def _get_single_result(self, cursor: pymongo.CursorType):
        result = list(cursor)
        if (len(result) > 1):
            raise NotSingleResultError(f"Query returned more than one result. Actual result: {list(cursor)}.")
        if (len(result) == 0):
             return None
        return result[0]