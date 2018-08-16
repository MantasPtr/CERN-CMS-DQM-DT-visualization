from validators.validation import validateRun

class RunContainer():
    def __init__(self, run, wheel, sector, station):
       validateRun(run, sector, station, wheel)
       self.run = run
       self.wheel = wheel
       self.sector = sector
       self.station = station

    def toDicts(self) -> (dict, dict):
        identifier = {"run":self.run}
        params = {"wheel": self.wheel, "sector": self.station, "station": self.station}
        return identifier, params
