from validotors.urlParamValidators import SectorValidator, StationValidator, WheelValidator
from validotors.abstractValidator import validateAndRaiseException

URL_BASE = "https://cmsweb.cern.ch/dqm/online/jsonfairy/archive/{0}/Global/Online/ALL/DT/01-Digi/Wheel{1}/Sector{2}/Station{3}/OccupancyAllHits_perCh_W{1}_St{3}_Sec{2}"

def buildUrl(testNumber, wheel ,sector, station ):
    validateParams(wheel, sector, station)
    return URL_BASE.format(testNumber,wheel,sector,station)

def validateParams( wheel ,sector, station ): 
    validateAndRaiseException(wheel, WheelValidator)
    validateAndRaiseException(sector, SectorValidator)
    validateAndRaiseException(station, StationValidator)
    

    


    
