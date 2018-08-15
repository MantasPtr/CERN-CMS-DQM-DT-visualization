from config.configUtils import getJsonConfig, getConfig
import json
import itertools 

def getStructureDict():
    return getJsonConfig("config/param.config.json")

structureConfig: dict = getStructureDict()
url = getConfig(configLocation="config/fetch.config.ini")["url"]

def getParamDicts():
    parameters = None
    for key in structureConfig.keys():
        if structureConfig[key]["type"] == "static":
            parameters = handleStaticParams(key, parameters)
        if structureConfig[key]["type"] == "dependant":
            parameters = handleDependantParams(key, parameters)                    
    return parameters

def handleStaticParams(key, parameters):
    paramRange = range(structureConfig[key]["min"], structureConfig[key]["max"]+1)
    if (parameters is None):
        parameters = [{key:value} for value in paramRange]
    else:
        parameters = [dict(oldDict,**{key:newValue}) for oldDict in parameters for newValue in paramRange]
    return parameters

def handleDependantParams(key, parameters):
    dependentOn = structureConfig[key]["on"]
    newParamDict = []
    for oldParam in parameters:
        for value in structureConfig[key]["values"]:
            if oldParam[dependentOn] in value["if_values"]:
                paramRange = range(value["min"],value["max"]+1)
                newParamDict.extend([dict(oldParam,**{key:newValue}) for newValue in paramRange])                   
    return newParamDict

def getUrlsGenerator(run: []):
    for params in getParamDicts():
        yield url.format(*run,**params), params
