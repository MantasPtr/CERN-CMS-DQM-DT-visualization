import ssl
import json
import aiohttp
from config import configUtils
from errors.errors import FetchError
from dataLoading.authContainer import AuthContainer
from errors.errors import ConfigError
import time
FETCH_CONFIG_LOCATION="dataLoading/config/fetch.config.ini"
PATH_STEPS = configUtils.getConfig(FETCH_CONFIG_LOCATION)["matrixJsonPath"].split(".")

class AsyncRequestExecutor():
    
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        authObj = AuthContainer().load_data()
        self.ssl_context = self._get_ssl_context(authObj)
        
    async def get_matrix_from_protected_url(self, url):
        dataJson = await self._get_json_data_from_protected_url(url)
        return self._get_matrix(self._parse_json(dataJson, url))

    async def _get_json_data_from_protected_url(self, url):
        print(time.time())
        result =  await self.session.get(url, ssl=self.ssl_context)
        return await result.content.read()

    def _get_ssl_context(self, authObj):
        context = ssl.SSLContext()
        try:
            context.load_cert_chain(authObj.pathToCertificate, authObj.pathToCertificatePass, authObj.password)
        except ssl.SSLError as exc:
            raise ConfigError(f"Error occurred while loading certificates. Please make sure all files are in locations defined in config and password is correct. Original error: {exc}")
        return context

    def _parse_json(self, dataJson, url):
        try:
            return json.loads(dataJson)
        except ValueError as ve:
            raise FetchError(f"Invalid json structure from url:{url} \n Error: {ve}")

    def _get_matrix(self, valueDictionary):
        currentJsonLocation = valueDictionary
        for index, step in enumerate(PATH_STEPS):
            currentJsonLocation = currentJsonLocation.get(step)
            if index != len(PATH_STEPS) - 1 and not isinstance(currentJsonLocation, dict):
                raise FetchError("Cannot load data from URL: Invalid json structure: " + str(valueDictionary) )
        return currentJsonLocation    
