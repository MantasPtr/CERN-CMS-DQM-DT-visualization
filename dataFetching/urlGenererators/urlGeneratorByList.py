from config.configUtils import getJsonConfig, getConfig
import json
import warnings 
from typing import Generator

structureConfig: dict = getJsonConfig("dataFetching/config/param.list.config.json")
url = getConfig("dataFetching/config/fetch.config.ini")["url"]

def get_url_generator(identifier: dict):
    """Generates urls to fetch data for each identifier based on params provided at param.config file"""
    param_dicts = _get_param_dicts()
    if (param_dicts is not None):
        for params in _get_param_dicts():
            yield url.format(**identifier,**params), params
    else:
        yield url.format(**identifier), None

def _get_param_dicts():
    parameters = None
    for key in structureConfig.keys():
        if structureConfig[key]["type"] == "static":
            parameters = _handle_static_params(key, parameters)
        elif structureConfig[key]["type"] == "dependant":
            parameters = _handle_dependant_params(key, parameters)
        else: 
            warnings.warn(f"unrecognized param type {structureConfig[key]['type']}")
    return parameters

def _handle_static_params(key, parameters):
    valueArray = structureConfig[key]["values"]
    if (parameters is None):
        parameters = [{key:value} for value in structureConfig[key]["values"]]
    else:
        parameters = _extend_with_new_params_combinations(parameters, key, valueArray)
    return parameters

def _extend_with_new_params_combinations(parameters, key, valueArray):
    return [dict(oldDict,**{key:newValue}) for oldDict in parameters for newValue in valueArray]

def _handle_dependant_params(key, parameters):
    dependentOn = structureConfig[key]["on"]
    newParamDict = []
    for oldParam in parameters:
        for dependency in structureConfig[key]["values"]:
            if oldParam[dependentOn] in dependency["if_values"]:
                valueArray = dependency["values"]
                newParamDict.extend([dict(oldParam,**{key:newValue}) for newValue in valueArray])                   
    return newParamDict