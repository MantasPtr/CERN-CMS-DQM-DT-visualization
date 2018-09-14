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

    def save(self, identifier: dict, status: str, data = None, other: dict = {}):
        record = self._build_db_record(identifier, data, status)
        record = self._add_other_fields(record, other)
        self.dbCollection.save(record)

    def update(self, identifier: dict, status: str, data = None, other: dict = {}):
        record = self._build_db_record(identifier, data, status)
        record = self._add_other_fields(record, other)
        self._assure_update({"identifier": identifier}, record)
    
    def update_status(self, identifier: dict, status: str, other: dict = {}):
        return self._assure_update({   
                "identifier": identifier, 
            },{
                "$set": {"status": status, **other}
            })

    def update_user_score(self, identifier: dict, param_dict: dict, bad_layers: list):
        return self._assure_update({   
                "identifier": identifier, 
                "data": {"$elemMatch": { ("params."+str(key)):value for key,value in param_dict.items() }}
            },{
                "$set": {"data.$.evaluation.bad_layers": bad_layers, "data.$.evaluation.eval_time": datetime.datetime.utcnow(), "data.$.evaluation.skipped":False}
            })

    def skip_user_score(self, identifier: dict, paramDict: dict):
        return self._assure_update({   
                "identifier": identifier, 
                "data": {"$elemMatch": { ("params."+str(key)):value for key,value in paramDict.items() }}
            },{
                "$set": {"data.$.evaluation.skipped": True}
            })

    def delete(self, identifier: dict):
        print("deleting:",identifier)
        rez = self.dbCollection.delete_one({"identifier": identifier})
        return rez.deleted_count

    def get_one(self, identifier: dict):
        return self.dbCollection.find_one({"identifier": identifier})

    def get_all(self):
        data = self.dbCollection.find(
            {}, 
            {"_id": 0}
        ).sort("save_time", pymongo.DESCENDING)
        return list(map(self._format_db_result_datatime, data))

    def _format_db_result_datatime(self, record: dict):
        datatime = record["save_time"] + self.timeOffset
        record["save_time"]= "%d-%02d-%02d %02d:%02d:%02d" % (datatime.year, datatime.month, datatime.day, datatime.hour, datatime.minute, datatime.second)
        return record

    def get_single_record_matrix(self, identifier: dict, paramsDict: dict):
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
        """returns: 
            [
                data: 
                    evaluation:
                        bad_layers: [<int?>]
                        eval_time:	<datatime>
                        skipped:    <boolean>
                    params:
                        sector:     <int>
                        station:    <int>
                        wheel:      <int>
                identifier:
                    run: <int>
            ]	
        """
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
                "data.evaluation.bad_layers":1,
                "data.evaluation.skipped":1,
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

    def _build_db_record(self, identifier: dict, data, status: str) -> dict:
        return {
            "identifier": identifier,
            "status": status,
            "save_time": datetime.datetime.utcnow(),
            "data": data
         }
     
    def _add_other_fields(self, data: dict, other: dict) -> dict:
        if bool(other): # if empty
            return data
        else:
            return {**data, **other}
        

    def _get_single_result(self, cursor: pymongo.CursorType):
        result = list(cursor)
        if (len(result) > 1):
            raise NotSingleResultError(f"Query returned more than one result. Actual result: {list(cursor)}.")
        if (len(result) == 0):
             return None
        return result[0]