from validators.validation import validateRun

def buildDicts(run, wheel: str, sector: int, station: int) -> (dict, dict):
    run = int(run)
    wheel = int(wheel)
    sector = int(sector)
    station = int(station)       
    validateRun(run, sector, station, wheel)
    identifier = {"run":run}
    params = {"wheel":wheel, "sector": sector, "station": station}
    return identifier, params
