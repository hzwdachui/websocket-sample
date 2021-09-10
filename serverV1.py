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
        await action(websocket)  # await 要等这个协程完成，这个协程在循环


async def action(websocket):
    '''
    建立一个连接以后的主逻辑
    '''
    while True:
        name = await websocket.recv()
        print(f"< {name}")

        greeting = f"Hello {name}!"

        await websocket.send(greeting)
        await broadcast(websocket_list, name)
        print(f"> {greeting}")

# todo
# 还需要一个协程，任何一个websocket收到信息都得往所有用户推送
async def broadcast(websocket_list, msg):
    for websocket in websocket_list:
        await websocket.send(msg)

def main():
    start_server = websockets.serve(handler, "localhost", 8002) # 每个请求都会起一个新的ws连接
    asyncio.get_event_loop().run_until_complete(start_server)
    print("start serving on localhost:8002")
    
    asyncio.get_event_loop().run_forever()
    
    

main()
