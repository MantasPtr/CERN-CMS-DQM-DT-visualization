import configparser

def getConfig(enviroment):
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config[enviroment]