import asyncio
import threading

def run_async_in_thread(function, *args):
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=_loop_in_thread, args=(loop, function, *args))
    t.start()

def _loop_in_thread(loop, function, *args):
    asyncio.set_event_loop(loop)
    rez = function(*args)
    f = asyncio.ensure_future(rez)
    loop.run_until_complete(f)