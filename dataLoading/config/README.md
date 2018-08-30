# Configuration for data loading

## auth.config.ini

* *pathToCert* global path to certificate file
* *pathToCert* global path to certificate key file
* *passwordFile* location to file that contains single line of password used for password protected certificates 

## fetch.config.ini

* *url* = url from which to fetch data form url. Has to have placeholders for literal string interpolation based on identifier and params to be filled by url_generator.
* *matrixJsonPath* = dot (.) separated path to matrix in retrieved json

## params.config.json

Json used to generate parameters for urls.

For now support 2 types of integer parameters: *static* and *dependant*

*static* generates values between the *min* and *max* [inclusively]:

```json
{
    "name":{
        "type": "static",
        "min": 0,
        "max": 100
    },
    {...}
}
```

*dependant* generates values between the *min* and *max* [inclusively] based on previously defined param values. Name and values of other field that this field is depending are defined in *on* and *if_values* fields .

```json
{
    {...},
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
    }
}
```