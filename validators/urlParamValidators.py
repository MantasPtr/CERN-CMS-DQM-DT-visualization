from validators.betweenValidator import BetweenValidator

PARAM_RANGES = { 
    "wheel": {
        "min": -2,
        "max": 2
    },
    "sector": {
        "min": 1,
        "max": 12
    },
    "station": {
        "min": 1,
        "max": 4
    }
}


class WheelValidator(BetweenValidator):
    minValue = PARAM_RANGES["wheel"]["min"]
    maxValue = PARAM_RANGES["wheel"]["max"]

    @classmethod
    def getErrorMessage(cls):
        return "Invalid wheel number: " + BetweenValidator.getErrorMessage(cls)

class SectorValidator(BetweenValidator):
    minValue = PARAM_RANGES["sector"]["min"]
    maxValue = PARAM_RANGES["sector"]["max"]

    @classmethod
    def getErrorMessage(cls):
        return "Invalid sector number: " + BetweenValidator.getErrorMessage(cls)

class StationValidator(BetweenValidator):
    minValue = PARAM_RANGES["station"]["min"]
    maxValue = PARAM_RANGES["station"]["max"]

    @classmethod
    def getErrorMessage(cls):
        return "Invalid station number: " + BetweenValidator.getErrorMessage(cls)