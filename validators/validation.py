from validators.urlParamValidators import SectorMB123Validator, SectorMB4Validator, StationValidator, WheelValidator
from validators.positiveValidator import PositiveValidator
from validators.abstractValidator import validateAndRaiseException


def validateRun(run, sector, station, wheel): 
    validateAndRaiseException(run, PositiveValidator)
    validateAndRaiseException(wheel, WheelValidator)
    validateAndRaiseException(station, StationValidator)
    if station != 4: 
        validateAndRaiseException(sector, SectorMB123Validator)
    else:
        validateAndRaiseException(sector, SectorMB4Validator)