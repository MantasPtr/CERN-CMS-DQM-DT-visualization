# from flask_socketio import send
# import asyncio

# async def sendTest(message):
#     print("Sending: " + message)
#     send(message, namespace='/fetch/listen')

# async def loopTest():
#     print("________Initalized test loop")
#     loop = asyncio.get_running_loop()
#     end_time = loop.time() + 5.0
#     while True:
#         sendTest("loop op")
#         if (loop.time() + 1.0) >= end_time:b
#             break
#         await asyncio.sleep(1)

# import asyncio
# import websockets

# async def testMessage(websocket, path):
#     print("__________SENDING!")
#     await websocket.send("Web socket")
#     print("__________SENT")
    

# def loopTest():
#     print("________STARTING WEB SOCKET")
#     start_server = websockets.serve(testMessage, '0.0.0.0/fetch/listen', 5000)
#     print("________STARTING event loop")
#     task = asyncio.get_event_loop().create_task(start_server)
#     print("________running event loop")
#     asyncio.get_event_loop().run_until_complete(task)
#     print("________FINISHED event loop")

import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)


def loopTest():
    print("________asdsdasd")
    pass

# print("==1")
# print(websockets.serve(echo, '0.0.0.0', 5001))
# print("==2")
# asyncio.get_event_loop().run_forever()
# print("==3")