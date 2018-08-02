from validators.validation import validateRun

class RunContainer():
   def __init__(self, run, wheel, sector, station):
       validateRun(run, sector, station, wheel)
       self.run = run
       self.wheel = wheel
       self.sector = sector
       self.station = station