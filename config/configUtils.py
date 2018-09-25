import configparser
import json
import warnings

DEFAULT_NOT_FOUND = {}

def getConfig(configLocation: str, key='DEFAULT'):
    config = configparser.ConfigParser()
    config.read(configLocation)
    return config[key]

def getJsonConfig(configLocation):
    try:
        with open(configLocation) as f:
            return json.load(f)
    except FileNotFoundError as fnfe:
        warnings.warn(f"Config file not found {configLocation}. Falling back to default value '{DEFAULT_NOT_FOUND}'")
        return DEFAULT_NOT_FOUND
