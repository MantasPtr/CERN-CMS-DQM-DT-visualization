# Configuration for data loading

## auth.config.ini

* *cert_path* - path from $HOME enviroment variable to certificate file
* *cert_key_path* - path from $HOME enviroment variable to certificate key file
* *password_file* - path from this folder to file that contains single line of password used for password protected certificates

## fetch.config.ini

* *url* - url from which to fetch data form. Has to have placeholders for literal string interpolation based on identifier and params to be filled by url_generator.
* *matrixJsonPath* - dot (.) separated path to matrix in from *url* retrieved json

## params.range.config.json

Json used to generate parameters for URLs. Values are defined in **ranges**.

For now support 2 types of integer parameters: *static* and *dependant*

*static* generates values between the *min* and *max* [inclusively]:

```json
    "name":{
        "type": "static",
        "min": 0,
        "max": 10
    },
```

*dependant* generates values between the *min* and *max* [inclusively] based on previously defined param values. Name and values of other field on which this field is depending are defined in *on* and *if_values* fields .

```json
    "name":{
        "type": "dependant",
        "on": "other_field_name",
        "values":[{
            "if_values": [1,2,3],
            "min": 1,
            "max": 10
        },{
            "if_values": [4],
            "min": 5,
            "max": 7
        }]
    },
```

## params.list.config.json

Json used to generate parameters for URLs. Values are defined in **list**.

For now support 2 types of integer parameters: *static* and *dependant*

*static* generates values from the *values* array:

```json
    "name":{
        "type": "static",
        "values": [0,1,2,3,4,5,6,7,8,9,10]
    },
```

*dependant* generates values between the from then *values* array based on previously defined param values. Name and values of other field on which this field is depending are defined in *on* and *if_values* fields .

```json
    "name":{
        "type": "dependant",
        "on": "other_field_name",
        "values":[{
            "if_values": [1,2,3],
            "values":[1,2,3,4,5,7,8,9,10]
        },{
            "if_values": [4],
            "values":[5,6,7]
        }]
    },
```
