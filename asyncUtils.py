import asyncio
import threading

def loop_in_thread(loop, function, *args):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(function(*args))

def run_in_thread(fuction, *args):
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=loop_in_thread, args=(loop, fuction, *args))
    t.start()