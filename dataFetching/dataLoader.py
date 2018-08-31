from dataFetching.asyncRequestExecutor import AsyncRequestExecutor
import asyncio
import aiohttp
from dataFetching.urlGenerator import get_url_generator

async def async_fetch_all_data(identifier: dict):
    tasks = []
    async with aiohttp.ClientSession() as client:
        executor = AsyncRequestExecutor(client)
        for url, params in get_url_generator(identifier):
            asyncLoadTask = async_load(url, params, executor)
            tasks.append(asyncLoadTask)
        return await asyncio.gather(*tasks)

async def async_load(url, paramDict, executor):
    matrix = await executor.get_matrix_from_protected_url(url)
    return _format_matrix_result(paramDict, matrix) 

def _format_matrix_result(params, matrix, scores=[]):
    return {
        "params": params,
        "matrix": matrix,
        "scores": scores
    }