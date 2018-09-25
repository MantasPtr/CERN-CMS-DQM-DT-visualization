import config.configUtils as cfg
from os.path import isfile
import pathlib
import warnings

AUTH_CONFIG_FILE = 'auth.config.ini'

class AuthContainer():
    certificate_path = None
    certificate_pass_path = None
    password = None

    def load_data(self):
        config_dir = pathlib.Path(__file__).parent / "config"
        config = cfg.getConfig(config_dir / AUTH_CONFIG_FILE)
        self.certificate_path = self._assure_file_path(config_dir /config['cert_path'], "Certificate")
        self.certificate_pass_path = self._assure_file_path( config_dir / config['cert_key_path'], "Certificate password")
        self.password = self._read_password_file(config_dir / config['password_file'])
        return self

    def _assure_file_path(self, path: pathlib.Path, file_purpose: str):
        if path.is_file():
            print(f"Error info: File was searched at {path}")
            raise FileNotFoundError(f"{file_purpose} file not found")
        return path

    def _read_password_file(self, file: pathlib.Path):
        if not file.is_file():
            warnings.warn("Password file not found", RuntimeWarning)
            return ""
        f = open(file,"r")
        return f.read()

    def with_home(self, path: pathlib.Path):
        return str(pathlib.Path.home()) + str(path)

container = AuthContainer()