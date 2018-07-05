from validotors.betweenValidator import BetweenValidator

class WheelValidator(BetweenValidator):
    minValue = -2
    maxValue = 2

    @classmethod
    def getErrorMessage(cls):
        return "Invalid wheel number:" + cls.getErrorMessage()

class SectorValidator(BetweenValidator):
    minValue = 1
    maxValue = 14

    @classmethod
    def getErrorMessage(cls):
        return "Invalid sector number:" + cls.getErrorMessage()

class StationValidator(BetweenValidator):
    minValue = 1
    maxValue = 4

    @classmethod
    def getErrorMessage(cls):
        return "Invalid station number:" + cls.getErrorMessage()