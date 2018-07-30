from validators.urlParamValidators import PARAM_RANGES, getSectorRangeDict
from dataLoading.urlBuilder import buildUrl
from dataLoading.asyncRequestExecutor import getSingletonExecutor
import asyncio

# def fetchAllRunData(runNumber):
#     #TODO: async
#     data = []
#     for wheel in range(PARAM_RANGES["wheel"]["min"], PARAM_RANGES["wheel"]["max"]+1):
#         for station in range(PARAM_RANGES["station"]["min"], PARAM_RANGES["station"]["max"]+1):
#             rangeDict = getSectorRangeDict(station) 
#             for sector in range(rangeDict["min"], rangeDict["max"]+1):
#                 url = buildUrl(runNumber, wheel, sector, station)
#                 matrix = getMatrixFromProtectedUrl(url)
#                 matrixResult = formatMatrixResult(wheel, sector, station, matrix)
#                 data.append(matrixResult)
#     return data
async def fetchAllRunDataAsync(runNumber):
    result = await asyncFetchAllRunData(runNumber)
    return result


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
    matrix = await getSingletonExecutor().getMatrixFromProtectedUrl(url)
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
