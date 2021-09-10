from asyncio import tasks
import websockets
import asyncio
from concurrent.futures.thread import ThreadPoolExecutor

username = ""
msg_list = []


def always_input():
    while True:
        text = input("input here: ")
        msg_list.append(text)
        


async def async_input():
    await asyncio.get_running_loop().run_in_executor(
        ThreadPoolExecutor(1),
        always_input
    )


async def send(websocket):
    print("start sending")
    while True:
        if len(msg_list) > 0:
            msg = msg_list.pop()
            await websocket.send(msg)
        else:
            await asyncio.sleep(1)
        


async def recv(websocket):
    print("start receiving")
    while True:
        greeting = await websocket.recv()
        print(f"< {greeting}")


async def action(websocket):
    task1 = asyncio.create_task(send(websocket))
    task2 = asyncio.create_task(recv(websocket))
    task3 = asyncio.create_task(async_input())
    # while True:
    await task1
    await task2
    await task3


async def main():
    username = input("username:")
    uri = f"ws://127.0.0.1:8002/{username}"
    async with websockets.connect(uri) as websocket:
        await action(websocket)

asyncio.run(main())
asyncio.get_event_loop().run_until_complete(main())
