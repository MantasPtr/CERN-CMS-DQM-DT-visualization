# CERN-CMS-DQM-DT-visualization

This is project I did during summer internship at European Organization for Nuclear Research.

This application was developed for visualizing data from compact muon solenoid data quality monitoring drift tube chambers.

## Structure

Modules by order of significance:

* `logic` - contains main program logic which connects all modules
* `database` - module for responsible for persisting data
* `dataFetching` - module for fetching data from external api
* `machineLearning` - module for processing data with neural network
* `config` - common config functions
* `errors`  - contains all custom error throw by application
* `gui` - contains flask templates and js files used for visualization
* `validators` - contains validation logic clases

Files:

* `asyncUtils` - utils for running functions asynchronously or in thread
* `flaskController` - flask app for serving front end

## App setup

### Installing mongoDB 4.0

Based on
<https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/>

### Opening port on in iptables

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
    "data": [{
            "params": {
                "wheel":0,
                "station":1,
                "sector":1
            },
            "matrix": [[0,0,0],[1,1,1],[777,888,999]],
            "scores": [0,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,1],
            "saliency": [[0,0,0],[1,2,3],[-1,-2,-3]],
            "evaluation": {
                "bad_layers": [1,7,14],
                "eval_time": "timestamp",
                "skipped": false
            }
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