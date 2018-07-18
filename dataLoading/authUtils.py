import config.configUtils as cfg
from os.path import isfile
import warnings

class AuthContainer():
    pathToCerticate = None
    pathToCerticatePass = None
    password = None

    @staticmethod
    def readPasswordFile(file):
        if not isfile(file):
            warnings.warn('Password file file not found', RuntimeWarning)
            return ''
        f = open(file,'r')
        return f.read()

    def loadData(self):
        config = cfg.getConfig()
        homePath = cfg.getHomePath()
        self.pathToCerticate= homePath + config['pathToCert']
        self.pathToCerticatePass= homePath + config['pathToCertKey']
        self.password= self.readPasswordFile(config['passwordFile'])
        return self

