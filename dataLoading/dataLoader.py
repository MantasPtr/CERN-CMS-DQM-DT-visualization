from dataLoading.asyncRequestExecutor import asyncRequestExecutor
import asyncio
import aiohttp
from dataLoading.urlGenerator import get_url_generator

async def async_fetch_all_data(identifier: dict):
    tasks = []
    async with aiohttp.ClientSession() as client:
        executor = asyncRequestExecutor(client)
        for url, params in get_url_generator(identifier):
            asyncLoadTask = async_load(url, params, executor)
            tasks.append(asyncLoadTask)
        return await asyncio.gather(*tasks)

async def async_load(url, paramDict, executor):
    matrix = await executor.getMatrixFromProtectedUrl(url)
    return _format_matrix_result(paramDict, matrix) 

def _format_matrix_result(params, matrix, scores=[]):
    return {
        "params": params,
        "matrix": matrix,
        "scores": scores
    }