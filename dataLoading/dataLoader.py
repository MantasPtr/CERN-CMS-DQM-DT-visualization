from validators.urlParamValidators import PARAM_RANGES 
from dataLoading.urlBuilder import buildUrl
from dataLoading.requestExecutor import getMatrixFromProtectedUrl

def fetchAllRunData(runNumber):
    #TODO: async
    data = []
    for wheel in range(PARAM_RANGES["wheel"]["min"], PARAM_RANGES["wheel"]["max"]+1):
        for sector in range(PARAM_RANGES["sector"]["min"], PARAM_RANGES["sector"]["max"]+1):
            for station in range(PARAM_RANGES["station"]["min"], PARAM_RANGES["station"]["max"]+1):
                url = buildUrl(runNumber, wheel, sector, station)
                matrix = getMatrixFromProtectedUrl(url)
                matrixResult = formatMatrixResult(wheel, sector, station, matrix)
                data.append(matrixResult)
    return data

def formatMatrixResult(wheel, sector, station, matrix):
    return {
        "params": {
            "wheel":wheel,
            "sector":sector,
            "station":station   
        },
        "matrix": matrix
    }
