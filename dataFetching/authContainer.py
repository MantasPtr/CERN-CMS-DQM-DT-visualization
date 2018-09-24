import config.configUtils as cfg
from os.path import isfile
import warnings

AUTH_CONFIG_LOCATION = 'dataFetching/config/auth.config.ini'

class AuthContainer():
    certificate_path = None
    certificate_pass_path = None
    password = None

    def load_data(self):
        config = cfg.getConfig(AUTH_CONFIG_LOCATION)
        homePath = cfg.getHomePath()
        self.certificate_path = self._assure_file_path( homePath + config['cert_path'], "Certificate")
        self.certificate_pass_path = self._assure_file_path(homePath + config['cert_key_path'], "Certificate password")
        self.password = self._read_password_file(config['password_file'])
        return self

    def _assure_file_path(self, path: str, file_purpose: str):
        if not isfile(path):
            print(f"Error info: File was searched at {path}")
            raise FileNotFoundError(f"{file_purpose} file not found")
        return path

    def _read_password_file(self, file):
        if not isfile(file):
            warnings.warn('Password file file not found', RuntimeWarning)
            return ''
        f = open(file,'r')
        return f.read()

container = AuthContainer()