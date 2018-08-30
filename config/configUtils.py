import configparser
import json
from pathlib import Path

def getConfig(configLocation: str, key='DEFAULT'):
    config = configparser.ConfigParser()
    parsed = config.read(configLocation)
    print(parsed)
    return config[key]

def getJsonConfig(configLocation):
    with open(configLocation) as f:
        return json.load(f)

def getHomePath():
    return str(Path.home())