from validotors.abstractValidator import AbstractValidator
from validotors.betweenValidator import BetweenValidator 

URL_BASE = "https://cmsweb.cern.ch/dqm/online/jsonfairy/archive/{0}/Global/Online/ALL/DT/01-Digi/Wheel{1}/Sector{2}/Station{3}/OccupancyAllHits_perCh_W{1}_St{3}_Sec{2}"

def buildUrl(testNumber, wheel ,sector, station ):
    return URL_BASE.format(testNumber,wheel,sector,station)

class WheelValidator(BetweenValidator):
    def __init__(self):
        self.min = -2
        self.max = 2

    def getErrorMessage(self):
        return "Invalid wheel number:" + BetweenValidator.getErrorMessage(self)

class SectorValidator(BetweenValidator):
    def __init__(self):
        self.min = 1
        self.max = 14

    def getErrorMessage(self):
        return "Invalid sector number:" + BetweenValidator.getErrorMessage(self)

class StationValidator(BetweenValidator):
    def __init__(self):
        self.min = 1
        self.max = 4

    def getErrorMessage(self):
        return "Invalid station number:" + BetweenValidator.getErrorMessage(self)




    
