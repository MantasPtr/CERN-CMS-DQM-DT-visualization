import urllib.request as request
import ssl
import configUtils
import json
import authUtils
import plotUtils

REQUEST_URL= "https://cmsweb.cern.ch/dqm/online/jsonfairy/archive/317111/Global/Online/ALL/DT/01-Digi/Wheel-1/Sector2/Station1/OccupancyAllHits_perCh_W-1_St1_Sec2"

def getLabelsFromProtectedUrl(url=REQUEST_URL):
    print("URL:", url)
    authObj = authUtils.AuthContainer().loadData()
    dataJson = getContentFromProtectedUrl(url, authObj)
    return getLabels(parseJsonResult(dataJson))

def getContentFromProtectedUrl(url, authObj: authUtils.AuthContainer): 
    context = ssl.SSLContext()
    context.load_cert_chain(authObj.pathToCerticate, authObj.pathToCerticatePass, authObj.password)
    return request.urlopen(url, context=context).read()

def getLabels(valueDictionary):
    hist = valueDictionary.get('hist')
    if isinstance(hist, str):
        raise ValueError("cannot load data from url")
    return valueDictionary.get('hist').get('bins').get('content')      


def parseJsonResult(jsonString):
    return json.loads(jsonString)