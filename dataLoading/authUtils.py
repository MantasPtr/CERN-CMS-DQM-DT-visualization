import config.configUtils as cfg
from os.path import isfile
import warnings

class AuthContainer():
    pathToCertificate = None
    pathToCertificatePass = None
    password = None

    def load_data(self):
        config = cfg.getConfig()
        homePath = cfg.getHomePath()
        self.pathToCertificate = homePath + config['pathToCert']
        self.pathToCertificatePass = homePath + config['pathToCertKey']
        self.password = self._read_password_file(config['passwordFile'])
        return self

    def _read_password_file(self, file):
        if not isfile(file):
            warnings.warn('Password file file not found', RuntimeWarning)
            return ''
        f = open(file,'r')
        return f.read()

container = AuthContainer()