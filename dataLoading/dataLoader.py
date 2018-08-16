from dataLoading.asyncRequestExecutor import asyncRequestExecutor
import asyncio
import aiohttp
import machineLearning.model as model
from dataLoading.parameterController import getUrlsGenerator

async def asyncFetchAllData(identifier: dict):
    tasks = []
    async with aiohttp.ClientSession() as client:
        executor = asyncRequestExecutor(client)
        for url, params in getUrlsGenerator(identifier):
            asyncLoadTask = asyncLoad(url, params, executor)
            tasks.append(asyncLoadTask)
        return await asyncio.gather(*tasks)

async def asyncLoad(url, paramDict, executor):
    matrix = await executor.getMatrixFromProtectedUrl(url)
    scores = model.getScoreForMatrix(matrix).tolist()
    return formatMatrixResult(paramDict, matrix, scores) 

def formatMatrixResult(params, matrix, scores=[]):
    return {
        "params": params,
        "matrix": matrix,
        "scores": scores
    }