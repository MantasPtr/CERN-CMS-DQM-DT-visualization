from validators.urlParamValidators import PARAM_RANGES, getSectorRangeDict
from dataLoading.urlBuilder import buildUrl
from dataLoading.asyncRequestExecutor import asyncRequestExecutor
import asyncio
import aiohttp
import machineLearning.model as model

async def asyncFetchAllRunData(runNumber):
    tasks = []
    async with aiohttp.ClientSession() as client:
        executor = asyncRequestExecutor(client)
        for wheel in range(PARAM_RANGES["wheel"]["min"], PARAM_RANGES["wheel"]["max"]+1):
            for station in range(PARAM_RANGES["station"]["min"], PARAM_RANGES["station"]["max"]+1):
                rangeDict = getSectorRangeDict(station) 
                for sector in range(rangeDict["min"], rangeDict["max"]+1):
                    asyncLoadTask = asyncLoad(runNumber, wheel, sector, station, executor)
                    tasks.append(asyncLoadTask)
        return await asyncio.gather(*tasks)
    
async def asyncLoad(runNumber, wheel, sector, station, executor):
    url = buildUrl(runNumber, wheel, sector, station)
    matrix = await executor.getMatrixFromProtectedUrl(url)
    scores = model.getScoreForMatrix(matrix).tolist()
    return formatMatrixResult(wheel, sector, station, matrix, scores) 
    
def formatMatrixResult(wheel, sector, station, matrix, scores):
    return {
        "params": {
            "wheel":wheel,
            "sector":sector,
            "station":station   
        },
        "matrix": matrix,
        "scores": scores
    }
