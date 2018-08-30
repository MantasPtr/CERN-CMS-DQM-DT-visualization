import ssl
import json
import aiohttp
from config import configUtils
from errors.errors import FetchError
from dataLoading.authContainer import AuthContainer
from errors.errors import ConfigError

FETCH_CONFIG_LOCATION="dataLoading/config/fetch.config.ini"

class asyncRequestExecutor():
    
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def getMatrixFromProtectedUrl(self, url):
        dataJson = await self.getJsonDataFromProtectedUrl(url)
        return self.getMatrix(self.parseJson(dataJson, url))

    def parseJson(self, dataJson, url):
        try:
            return json.loads(dataJson)
        except ValueError as ve:
            raise FetchError(f"Invalid json structure from url:{url} \n Error: {ve}")

    async def getJsonDataFromProtectedUrl(self, url):
        authObj = AuthContainer().load_data()
        return await self.getContentFromProtectedUrl(url, authObj)

    async def getContentFromProtectedUrl(self, url, authObj: AuthContainer): 
        context = ssl.SSLContext()
        try:
            context.load_cert_chain(authObj.pathToCertificate, authObj.pathToCertificatePass, authObj.password)
        except ssl.SSLError as exc:
            raise ConfigError(f"Error occurred while loading certificates. Please make sure all files are in locations defined in config and password is correct. Original error: {exc}")

        result =  await self.session.get(url, ssl=context)
        return await result.content.read()

    def getMatrix(self, valueDictionary):
        jsonPath = configUtils.getConfig(FETCH_CONFIG_LOCATION)["matrixJsonPath"]
        pathSteps = jsonPath.split(".")
        currentJsonLocation = valueDictionary
        for index, step in enumerate(pathSteps):
            currentJsonLocation = currentJsonLocation.get(step)
            if index != len(pathSteps) - 1 and not isinstance(currentJsonLocation, dict):
                raise FetchError("Cannot load data from URL: Invalid json structure: " + str(valueDictionary) )
        return currentJsonLocation    
