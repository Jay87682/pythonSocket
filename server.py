#!/usr/bin/env python

# WS server example
import threading
import asyncio
import websockets
import logging
import time


async def send_msg(websocket):
    while True:
        send_cmd = input('Type something to send client\n')
        print('send something')
        if (send_cmd == 'close'):
            print('close client')
            break
        elif (send_cmd != ''):
            print('sending')
            await websocket.send(send_cmd)
            print(f"> {send_cmd}")

def send_msg_thread(websocket):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(send_msg(websocket))


async def hello(websocket, path):
    thread = threading.Thread(target=send_msg_thread, args=(websocket,))
    thread.start()
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
    start_server = websockets.serve(hello, "0.0.0.0", "8888", ping_interval=None)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

thread = threading.Thread(target=process, daemon=True)
thread.start()
while True:
    print("main...")
    time.sleep(1 * 60 * 1000)
#    exit_signal = input('Type "exit" anytime to stop server\n')
#    if exit_signal != '':
#        break
#
