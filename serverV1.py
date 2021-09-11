import asyncio
import websockets

user_list = []
websocket_list = []


async def handler(websocket, path):
    if path in user_list:
        pass
    else:
        print(f"new user {path}")
        user_list.append(path)
        websocket_list.append(websocket)
        await action(websocket, path)


async def action(websocket, path):
    '''
    建立一个连接以后的主逻辑
    '''
    while True:
        text = await websocket.recv()
        broadcast_text = f"{path}: {text}"
        await broadcast(websocket_list, broadcast_text)
        print(f"{broadcast_text}")


async def broadcast(websocket_list, msg):
    for websocket in websocket_list:
        await websocket.send(msg)


def main():
    start_server = websockets.serve(
        handler, "localhost", 8002)  # 每个请求都会起一个新的ws连接
    asyncio.get_event_loop().run_until_complete(start_server)
    print("start serving on localhost:8002")

    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()

    # todo: secure tsl
    # todo: handle closing and exception
    # todo: use official websockets.broadcase