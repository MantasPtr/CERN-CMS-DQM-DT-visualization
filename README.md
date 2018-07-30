## Installing mongoDB 4.0

Based on https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/

## Opening port on inptables

by default using port 5000

```bash
sudo iptables -I INPUT -p tcp --dport 5000 -j ACCEPT
```

## Database format

```json
{  
    "_id" : "AUTO-GENERATED",
    "run" : 123456,
    "status": "loading | finished",
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

* "run" field contains unique index!
* status has one of values - "loading" - if data is still fetching or "finished" - if data is fully loaded
* matrix is empty if status is "loading"