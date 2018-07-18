import configparser
from pathlib import Path

def getConfig(enviroment='DEFAULT', configLocation='config/config.ini'):
    config = configparser.ConfigParser()
    config.read(configLocation)
    return config[enviroment]

def getHomePath():
    return str(Path.home())