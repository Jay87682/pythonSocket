#!/usr/bin/env python

# WS server example
import threading
import asyncio
import websockets
import logging

async def hello(websocket, path):
    while True:
        print("hello")
        try:
            name = await websocket.recv()
            print(f"< {name}")
            greeting = f"Hello {name}!"
            await websocket.send(greeting)
            print(f"> {greeting}")
        except websockets.exceptions.ConnectionClosed:
            print('client close')
            break;

def process():
    print("process")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(hello, "127.0.0.1", "8888")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

thread = threading.Thread(target=process)
thread.daemon = True
thread.start()
while True:
    exit_signal = input('Type "exit" anytime to stop server\n')
    if exit_signal != '':
        break

