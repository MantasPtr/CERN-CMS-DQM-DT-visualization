# Installing mongoDB 4.0

Based on https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/

## Database format

```json
{  
    "_id" : "AUTO-GENERATED",
    "run" : "123456",
    "save_time": "timestamp",
    "data": [
        {
            "params": {
                "wheel":0,
                "station":1,
                "sector":1
            },
            "matrix": [[1,1,1],[1,1,1],[1,1,1]],
            "user_scores": [
               {
                 "good_layers":[1,2,14],
                 "eval_time": "timestamp"
               },
               {
                 "good_layers":[2,14],
                 "eval_time": "timestamp"
               }
            ]
        },
        {
            "params": {
                "wheel":0,
                "station":1,
                "sector":2
            },
            "matrix": [[1,1,1],[1,1,1],[1,1,1]]
        },
    ]
}
```