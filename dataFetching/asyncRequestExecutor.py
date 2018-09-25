import ssl
import json
import aiohttp
from config import configUtils
from errors.errors import FetchError
from dataFetching.authContainer import AuthContainer
from errors.errors import ConfigError
import time
FETCH_CONFIG_LOCATION="dataFetching/config/fetch.config.ini"
PATH_STEPS = configUtils.getConfig(FETCH_CONFIG_LOCATION)["matrixJsonPath"].split(".")

class AsyncRequestExecutor():
    
    def __init__(self, session: aiohttp.ClientSession, authContainer: AuthContainer):
        self.session = session
        self.ssl_context = self._init_ssl_context(authContainer)
        
    async def get_matrix_from_protected_url(self, url):
        dataJsonString = await self._get_json_data_from_protected_url(url)
        dataJson = self._parse_json(dataJsonString, url)
        return self._navigate_json_to_matrix(dataJson)

    async def _get_json_data_from_protected_url(self, url):
        result = await self.session.get(url, ssl=self.ssl_context)
        return await result.content.read()

    def _parse_json(self, dataJson, url):
        try:
            return json.loads(dataJson)
        except ValueError as ve:
            raise FetchError(f"Invalid json structure from url:{url} \n Error: {ve}")

    def _navigate_json_to_matrix(self, valueDictionary):
        currentJsonLocation = valueDictionary
        for index, step in enumerate(PATH_STEPS):
            currentJsonLocation = currentJsonLocation.get(step)
            if index != len(PATH_STEPS) - 1 and not isinstance(currentJsonLocation, dict):
                raise FetchError("Cannot load data from URL: Invalid json structure: " + str(valueDictionary) )
        return currentJsonLocation    

    def _init_ssl_context(self, authObj):
        context = ssl.SSLContext()
        try:
            context.load_cert_chain(authObj.with_home(authObj.certificate_path), authObj.with_home(authObj.certificate_pass_path), authObj.password)
        except ssl.SSLError as exc:
            raise ConfigError(f"Error occurred while loading certificates. Please make sure all files are in locations defined in config and password is correct. Original error: {exc}")
        return context