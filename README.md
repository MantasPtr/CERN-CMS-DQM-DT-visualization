## Installing mongoDB 4.0

Based on https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/

## Opening port on inptables

by default using port 8080 and redirecting to it from port 80

```bash
sudo iptables -I INPUT -p tcp --dport 8080 -j ACCEPT
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
```

## Database format

```json
{  
    "_id" : "AUTO-GENERATED",
    "identifier" : {"run":123456},
    "status": "LOADING | FINISHED | ERROR",
    "exception": "some exception",
    "save_time": "timestamp",
    "data": [       {
            "params": {
                "wheel":0,
                "station":1,
                "sector":1
            },
            "matrix": [[1,1,1],[1,1,1],[1,1,1]],
            "scores": [0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
            "user_scores": [
               {
                 "bad_layers":[1,2,12],
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

* "run" field contains unique index
* "status" has one of values:
  * LOADING - if data is still fetching
  * FINISHED - if data is fully loaded
  * ERROR - if error was encoutered while fetching
* "matrix" is empty unless status is "FINISHED"
* "exception" does not exist unless status is "ERROR"
* "scores" show how bad layers is according to neural network

### Warnings:

* Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
* UserWarning: Error in loading the saved optimizer state. As a result, your model is starting with a freshly initialized optimizer.