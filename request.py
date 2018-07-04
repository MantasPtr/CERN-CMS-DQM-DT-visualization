import urllib.request as request
import ssl
import configUtils

config = configUtils.getConfig('DEFAULT')
homePath = configUtils.getHomePath()
PATH_TO_CERT= homePath + config['pathToCert']
PATH_TO_CERT_KEY= homePath + config['pathToCertKey']
PASS=config['password']

REQUEST_URL= "https://cmsweb.cern.ch/dqm/online/jsonfairy/archive/317111/Global/Online/ALL/DT/01-Digi/Wheel-1/Sector2/Station1/OccupancyAllHits_perCh_W-1_St1_Sec2"
context = ssl.SSLContext()
context.load_cert_chain(PATH_TO_CERT, PATH_TO_CERT_KEY, PASS)

print (request.urlopen(REQUEST_URL, context=context).read())