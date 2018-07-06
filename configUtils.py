import configparser
from pathlib import Path

def getConfig(enviroment):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config[enviroment]

def getConfig(enviroment):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config[enviroment]

def getHomePath():
    return str(Path.home())