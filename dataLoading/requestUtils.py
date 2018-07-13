import urllib.request as request
import ssl
import json
from dataLoading import authUtils

DEMO_REQUEST_URL= "https://cmsweb.cern.ch/dqm/online/jsonfairy/archive/317111/Global/Online/ALL/DT/01-Digi/Wheel-1/Sector2/Station1/OccupancyAllHits_perCh_W-1_St1_Sec2"

def getLabelsFromProtectedUrl(url=DEMO_REQUEST_URL):
    dataJson = getDataJsonFromProtectedUrl(url)
    return getLabels(parseJsonResult(dataJson))

def getDataJsonFromProtectedUrl(url=DEMO_REQUEST_URL):
    print("URL" + url)
    authObj = authUtils.AuthContainer().loadData()
    return getContentFromProtectedUrl(url, authObj)

def getContentFromProtectedUrl(url, authObj: authUtils.AuthContainer): 
    context = ssl.SSLContext()
    context.load_cert_chain(authObj.pathToCerticate, authObj.pathToCerticatePass, authObj.password)
    return request.urlopen(url, context=context).read()

def getLabels(valueDictionary):
    hist = valueDictionary.get('hist')
    if isinstance(hist, str):
        raise ValueError("Cannot load data from url")
    return valueDictionary.get('hist').get('bins').get('content')      

def parseJsonResult(jsonString):
    return json.loads(jsonString)