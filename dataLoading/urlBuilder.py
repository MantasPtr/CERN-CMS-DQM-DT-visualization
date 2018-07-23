from validators.validation import validateRun
from dataLoading.paramContainer import ParamContainer


URL_BASE = "https://cmsweb.cern.ch/dqm/online/jsonfairy/archive/{0}/Global/Online/ALL/DT/01-Digi/Wheel{1}/Sector{2}/Station{3}/OccupancyAllHits_perCh_W{1}_St{3}_Sec{2}"

def buildFromContainer(container: ParamContainer):
    return buildUrl(container.run, container.wheel, container.sector, container.station)

def validateAndBuildUrl(runNumber, wheel ,sector, station ):
    validateRun(runNumber, sector, station, wheel)
    return buildUrl(runNumber, wheel, sector, station)

def buildUrl(run, wheel,sector,station):
    return URL_BASE.format(run, wheel, sector, station)

    


    
