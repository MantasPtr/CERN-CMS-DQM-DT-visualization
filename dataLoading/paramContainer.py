from validators.urlParamValidators import SectorValidator, StationValidator, WheelValidator
from validators.positiveValidator import PositiveValidator
from validators.abstractValidator import validateAndRaiseException

URL_BASE = "https://cmsweb.cern.ch/dqm/online/jsonfairy/archive/{0}/Global/Online/ALL/DT/01-Digi/Wheel{1}/Sector{2}/Station{3}/OccupancyAllHits_perCh_W{1}_St{3}_Sec{2}"

class ParamContainer:
    run:int =  None
    sector:int =  None
    station: int =  None
    wheel: int = None

    def __init__(self, runNumber: int , wheel: int ,sector: int, station: int):
        
        validateAndRaiseException(runNumber, PositiveValidator)
        validateAndRaiseException(wheel, WheelValidator)
        validateAndRaiseException(sector, SectorValidator)
        validateAndRaiseException(station, StationValidator)
        
        self.run = runNumber
        self.sector = wheel
        self.station = station
        self.wheel = wheel
    


    
