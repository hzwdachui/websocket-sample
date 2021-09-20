import asyncio
import websockets
from server_config import configs
import sys

user_list = []
websocket_list = []


async def handler(websocket, path):
    '''
    for each client trying to connect the server
    if not exists, launcing a connection
    '''
    try:
        if path in user_list:
            await websocket.close()
        else:
            user_list.append(path)
            websocket_list.append(websocket)
            await broadcast(websocket_list, f"{path} comes")
            print(f"{path} comes")   # debug
            await action(websocket, path)
    except websockets.exceptions.ConnectionClosedOK:
        websocket_list.remove(websocket)
        user_list.remove(path)
        await broadcast(websocket_list, f"{path} leaves")
        print(f"{path} leaves")  # debug
    except Exception as err:
        websocket_list.remove(websocket)
        user_list.remove(path)
        msg = f'{type(err).__name__}: {err}'
        print(msg)  # debug


async def action(websocket, path):
    '''
    the main logic after building connection
    '''
    while True:
        text = await websocket.recv()
        broadcast_text = f"{path}: {text}"
        await broadcast(websocket_list, broadcast_text)
        print(f"{broadcast_text}")  # debug


async def broadcast(websocket_list, msg):
    '''
    broadcasting msgs to all client
    '''
    for websocket in websocket_list:
        await websocket.send(msg)


def main():
    try:
        config_type = sys.argv[1]
        config = load_config(config_type)
        print(f"working on the {config_type} config")
    except IndexError:
        sys.stderr.write('please provide config type\n')
        return

    start_server = websockets.serve(
        handler, config.host, config.port)  # launch a new ws connection of each client
    asyncio.get_event_loop().run_until_complete(start_server)
    print(f"start serving on {config.host}:{config.port}")

    asyncio.get_event_loop().run_forever()


def load_config(config_type="debug"):
    try:
        config = configs[config_type]
        return config
    except Exception as err:
        print(f"please input a valid config type: {list(configs.keys())}")
        quit()


if __name__ == "__main__":
    main()
