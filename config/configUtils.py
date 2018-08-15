import configparser
import json
from pathlib import Path

def getConfig(key='DEFAULT', configLocation='config/auth.config.ini'):
    config = configparser.ConfigParser()
    config.read(configLocation)
    return config[key]

def getJsonConfig(configLocation):
    with open(configLocation) as f:
        return json.load(f)

def getHomePath():
    return str(Path.home())