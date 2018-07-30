from validators.urlParamValidators import PARAM_RANGES, getSectorRangeDict
from dataLoading.urlBuilder import buildUrl
import dataLoading.asyncRequestExecutor import requestExecutor
import asyncio

async def asyncFetchAllRunData(runNumber):
    tasks = []
    for wheel in range(PARAM_RANGES["wheel"]["min"], PARAM_RANGES["wheel"]["max"]+1):
        for station in range(PARAM_RANGES["station"]["min"], PARAM_RANGES["station"]["max"]+1):
             rangeDict = getSectorRangeDict(station) 
             for sector in range(rangeDict["min"], rangeDict["max"]+1):
                asyncLoadTask = asyncLoad(runNumber, wheel, sector, station)
                tasks.append(asyncLoadTask)
    return await asyncio.gather(*tasks)
    
async def asyncLoad(runNumber, wheel, sector, station):
    url = buildUrl(runNumber, wheel, sector, station)
    matrix = await requestExecutor.getMatrixFromProtectedUrl(url)
    return formatMatrixResult(wheel, sector, station, matrix)

def formatMatrixResult(wheel, sector, station, matrix):
    return {
        "params": {
            "wheel":wheel,
            "sector":sector,
            "station":station   
        },
        "matrix": matrix
    }
