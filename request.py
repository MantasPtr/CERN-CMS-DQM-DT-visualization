import urllib.request as request
import ssl
import configUtils
import json
import authUtils
import plotUtils


REQUEST_URL= "https://cmsweb.cern.ch/dqm/online/jsonfairy/archive/317111/Global/Online/ALL/DT/01-Digi/Wheel-1/Sector2/Station1/OccupancyAllHits_perCh_W-1_St1_Sec2"

def parseJsonResult(jsonString):
    return json.loads(jsonString)

def getLabels(valueDictionary):
    return valueDictionary.get('hist').get('bins').get('content')

def getDataFromProtectedUrl(url, authObj: authUtils.AuthContainer): 
    context = ssl.SSLContext()
    context.load_cert_chain(authObj.pathToCerticate, authObj.pathToCerticatePass, authObj.password)
    return request.urlopen(REQUEST_URL, context=context).read()

authObj = authUtils.AuthContainer().loadData()
dataJson = getDataFromProtectedUrl(REQUEST_URL, authObj)
labels = getLabels(parseJsonResult(dataJson))
print(labels)

plotUtils.plot(labels)

