from utils.logService import LogService
import asyncio
import websockets
from conf.server_config import configs
import sys
import os
sys.path.append(os.path.abspath('../'))
USER_LIST = []
WEBSOCKET_LIST = []
LOGGER = None


async def handler(websocket, path):
    '''
    for each client trying to connect the server
    if not exists, launcing a connection
    '''
    try:
        if path in USER_LIST:
            await websocket.close()
        else:
            USER_LIST.append(path)
            WEBSOCKET_LIST.append(websocket)
            await broadcast(WEBSOCKET_LIST, f"{path} comes")
            LOGGER.debug(f"{path} comes")
            await action(websocket, path)
    except websockets.exceptions.ConnectionClosedOK:
        WEBSOCKET_LIST.remove(websocket)
        USER_LIST.remove(path)
        await broadcast(WEBSOCKET_LIST, f"{path} leaves")
        LOGGER.debug(f"{path} leaves")
    except Exception as err:
        WEBSOCKET_LIST.remove(websocket)
        USER_LIST.remove(path)
        msg = f'{type(err).__name__}: {err}'
        LOGGER.debug(msg)


async def action(websocket, path):
    '''
    the main logic after building connection
    '''
    while True:
        text = await websocket.recv()
        broadcast_text = f"{path}: {text}"
        await broadcast(WEBSOCKET_LIST, broadcast_text)
        LOGGER.debug(f"{broadcast_text}")


async def broadcast(WEBSOCKET_LIST, msg):
    '''
    broadcasting msgs to all client
    '''
    for websocket in WEBSOCKET_LIST:
        await websocket.send(msg)


def main():
    global LOGGER
    try:
        config_type = sys.argv[1]
        config = load_config(config_type)
        LOGGER = LogService(config_type).getLogger()
        LOGGER.info(f"working on the {config_type} config")
    except IndexError:
        sys.stderr.write('please provide config type\n')
        return

    start_server = websockets.serve(
        handler, config.host, config.port)  # launch a new ws connection of each client
    asyncio.get_event_loop().run_until_complete(start_server)
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
