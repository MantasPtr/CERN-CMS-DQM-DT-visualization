from validators.validation import validateRun
from logic.runContainer import RunContainer

URL_BASE = "https://cmsweb.cern.ch/dqm/online/jsonfairy/archive/{0}/Global/Online/ALL/DT/01-Digi/Wheel{1}/Sector{2}/Station{3}/OccupancyAllHits_perCh_W{1}_St{3}_Sec{2}"

def buildUrlFromContainer(runContainer :RunContainer):
    return buildUrl(runContainer.run, runContainer.wheel, runContainer.sector, runContainer.station)

def buildUrl(run, wheel, sector, station):
    return URL_BASE.format(run, wheel, sector, station)

