from validators.betweenValidator import BetweenValidator

PARAM_RANGES = { 
    "wheel": {
        "min": -2,
        "max": 2
    },
    "sectorMB123": {
        "min": 1,
        "max": 12
    },
    "sectorMB4": {
        "min": 1,
        "max": 14
    },  
    "station": {
        "min": 1,
        "max": 4
    }
}

def getSectorRangeDict(station):
    if station == 4:
        return PARAM_RANGES["sectorMB4"]
    elif 0 < station <= 3:
        return PARAM_RANGES["sectorMB123"]
    else: 
        raise IndexError("Invalid station value")

class WheelValidator(BetweenValidator):
    minValue = PARAM_RANGES["wheel"]["min"]
    maxValue = PARAM_RANGES["wheel"]["max"]

    @classmethod
    def getErrorMessage(cls):
        return "Invalid wheel number: " + BetweenValidator.getErrorMessage(cls)

class SectorMB123Validator(BetweenValidator):
    minValue = PARAM_RANGES["sectorMB123"]["min"]
    maxValue = PARAM_RANGES["sectorMB123"]["max"]

    @classmethod
    def getErrorMessage(cls):
        return "Invalid sector number: " + BetweenValidator.getErrorMessage(cls)

class SectorMB4Validator(BetweenValidator):
    minValue = PARAM_RANGES["sectorMB4"]["min"]
    maxValue = PARAM_RANGES["sectorMB4"]["max"]

    @classmethod
    def getErrorMessage(cls):
        return "Invalid sector number: " + BetweenValidator.getErrorMessage(cls)

class StationValidator(BetweenValidator):
    minValue = PARAM_RANGES["station"]["min"]
    maxValue = PARAM_RANGES["station"]["max"]

    @classmethod
    def getErrorMessage(cls):
        return "Invalid station number: " + BetweenValidator.getErrorMessage(cls)