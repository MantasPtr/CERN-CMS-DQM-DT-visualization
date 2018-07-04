import configUtils

class AuthContainer():
    pathToCerticate = None
    pathToCerticatePass = None
    password = None

    def loadData(self):
        config = configUtils.getConfig('DEFAULT')
        homePath = configUtils.getHomePath()
        self.pathToCerticate= homePath + config['pathToCert']
        self.pathToCerticatePass= homePath + config['pathToCertKey']
        self.password=config['password']
        return self