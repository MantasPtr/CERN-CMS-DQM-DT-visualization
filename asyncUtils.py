import asyncio
import threading

# def call_in_background(target, executor=None):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     target = asyncio.ensure_future(target)
#     if callable(target):
#         return loop.run_in_executor(executor, target)
#     raise TypeError(f"target must be a callable, not {type(target)}")
# 
# def call_coroutine(target, *, loop=None):
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     return asyncio.run_coroutine_threadsafe(target, loop=loop)

def loop_in_thread(loop, function, *args):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(function(*args))

def run_in_thread(fuction, *args):
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop, fuction, *args))
    t.start()