from threading import Thread
import websockets
import asyncio

username = ""


class SendThread(Thread):
    websocket = None

    def __init__(self, websocket):
        super().__init__()
        self.websocket = websocket

    def run(self):
        asyncio.run(self.always_input(self.websocket))

    async def always_input(self, websocket):
        print("start inputing")
        while True:
            text = input("input here: ")
            await websocket.send(text)


def send(websocket):
    '''
    handling input event
    input is blocking so using another thread
    '''
    t = SendThread(websocket)
    t.start()


async def recv(websocket):
    '''
    receiving msg from server
    '''
    print("start receiving")
    while True:
        text = await websocket.recv()
        print(f"{text}")


async def action(websocket):
    send(websocket)
    rect_task = asyncio.create_task(recv(websocket))
    await rect_task


async def main():
    '''
    communicating with server
    '''
    username = input("username:")
    uri = f"ws://127.0.0.1:8002/{username}"
    async with websockets.connect(uri) as websocket:
        await action(websocket)

asyncio.run(main())
