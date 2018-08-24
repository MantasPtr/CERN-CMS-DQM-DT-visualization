import ssl
import json
import aiohttp
from config import configUtils
from errors.errors import FetchError
from dataLoading import authUtils

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
        print("Request URL: " + url)
        authObj = authUtils.AuthContainer().load_data()
        return await self.getContentFromProtectedUrl(url, authObj)

    async def getContentFromProtectedUrl(self, url, authObj: authUtils.AuthContainer): 
        context = ssl.SSLContext()
        context.load_cert_chain(authObj.pathToCertificate, authObj.pathToCertificatePass, authObj.password)
        result =  await self.session.get(url, ssl=context)
        return await result.content.read()

    def getMatrix(self, valueDictionary):
        jsonPath = configUtils.getConfig(configLocation="config/fetch.config.ini")["matrixJsonPath"]
        pathSteps = jsonPath.split(".")
        currentJsonLocation = valueDictionary
        for index, step in enumerate(pathSteps):
            currentJsonLocation = currentJsonLocation.get(step)
            if index != len(pathSteps) - 1 and not isinstance(currentJsonLocation, dict):
                raise FetchError("Cannot load data from URL: Invalid json structure: " + str(valueDictionary) )
        return currentJsonLocation    
