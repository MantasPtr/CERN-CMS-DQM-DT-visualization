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
* `validators` - contains validation logic classes
* `utils` - contains utils which can be used individually in any module

Files:

* `flaskController` - flask app for serving front end

## App setup

Created using `Python 3.6`, `Flask`, `Jinja2`, `Javascript` and `HTML`/`CSS`

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
                "bad_layers": [1,0,0,0,0,0,1,0,0,0,0,1],
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
  * ERROR - if error was encountered while fetching
  * REEVALUATING - scores are being recomputed
  * PENDING_REEVALUATION - are being recomputed
* "matrix" is empty unless status is "FINISHED"
* "exception" does not exist unless status is "ERROR"
* "scores" show how bad layers is according to neural network

## End-points

### Pages

#### HTTP GET

* `/eval/` - renders evaluation page. This page is used to visualize the matrices and provide active learning capability.
* `/eval/<int:run>/` - renders evaluation page with "run" input field having the "run" value.
* `/eval/<int:run>/<int:wheel>/<int:sector>/<int:station>/` - renders evaluation page with "run","wheel","sector", "station" input fields having the values of `run`,`wheel`,`sector`,`station`. Automatically attempts to load matrix on load.
* `/eval/next` - returns next record which result should be evaluated according to active learning algorithm network scores.
* `/eval/skip` - returns marks current record as skipped, so it counts as evaluated and wont appear next to unevaluated results.
* `/fetch/` - renders fetch page template. It is used to initiate data fetching from external api and saving to local database.
* `/data/net_scores/` - renders page which shows network evaluation results.
* `/data/new_net_scores/` - renders page which shows network evaluation results which user has not evaluated yet.

#### HTTP PATCH

* url: `/eval/save_user_scores/`, body: `{"run":<int>,"wheel":<int>,"sector":<int>},"station":<int>,"layers":<array<int>>` - updates record with given parameters. `Layers` is array of indexes which should be marked as bad.

#### HTTP POST

* url: `/fetch/<int:run>/`, body:None  - if record with given record does not exit in database, initialize data fetching for specified run.
* If record with specified id exit in database returns error message and HTTP 409 ("CONFLICT")

### Data endpoints

#### HTTP GET

* `/data/<int:run>/<int:wheel>/<int:sector>/<int:station>/` - returns data for specified `run`, `wheel`, `sector` and `station`.
  * Returns HTTP 404, if record with specified parameters is not found
  * Returns HTTP 500, if record with specified parameters specified parameters matched not 1 result.  
* `/data/user_scores.json/` - returns which records have been evaluated and user evaluation scores.
* `/data/net_scores.json/` - returns records in order of network scores.
* `/data/reevaluate/` - reruns record evaluation using neural network.

#### HTTP DELETE

* `/data/<int:run>/` - delete record with specified `run` from database. Returns deleted record count.

### Other

#### HTTP GET

* `/visualize/<int:run>/<string:wheel>/<int:sector>/<int:station>/` - plots steps of creating saliency methods

### Active learning

* https://www.caiac.ca/sites/default/files/publications/Barnab%C3%A9-Lortie_Vincent_2015_thesis.pdf
* https://arxiv.org/pdf/1808.00911.pdf
* https://github.com/experiencor/deep-viz-keras

### Interesting bad run

* /eval/279794/2/12/1/
* bad web design /eval/279794/-2/1/4/

### Warnings

* Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
* UserWarning: Error in loading the saved optimizer state. As a result, your model is starting with a freshly initialized optimizer.