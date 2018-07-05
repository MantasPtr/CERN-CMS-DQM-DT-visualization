import urllib.request as request
import ssl
import configUtils
import json
import authUtils
import plotUtils


REQUEST_URL= "https://cmsweb.cern.ch/dqm/online/jsonfairy/archive/317111/Global/Online/ALL/DT/01-Digi/Wheel-1/Sector2/Station1/OccupancyAllHits_perCh_W-1_St1_Sec2"
URL_BASE = "https://cmsweb.cern.ch/dqm/online/jsonfairy/archive/{0}/Global/Online/ALL/DT/01-Digi/Wheel{1}/Sector{2}/Station{3}/OccupancyAllHits_perCh_W-{1}_St{2}_Sec{3}"

def getLabelsFromProtectedUrl(url=REQUEST_URL):
    authObj = authUtils.AuthContainer().loadData()
    dataJson = getContentFromProtectedUrl(url, authObj)
    return getLabels(parseJsonResult(dataJson))

def getContentFromProtectedUrl(url, authObj: authUtils.AuthContainer): 
    context = ssl.SSLContext()
    context.load_cert_chain(authObj.pathToCerticate, authObj.pathToCerticatePass, authObj.password)
    return request.urlopen(REQUEST_URL, context=context).read()

def getLabels(valueDictionary):
    return valueDictionary.get('hist').get('bins').get('content')

def parseJsonResult(jsonString):
    return json.loads(jsonString)


