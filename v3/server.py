import asyncio
import aiohttp
from aiohttp import web
import aiohttp_jinja2
import jinja2
from broadcaster import Broadcaster

broadcaster = Broadcaster()


@aiohttp_jinja2.template('index.html')
def chat_index(request):
    return {}


async def chat_websocket(request):
    tasks = []
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    subscriber = await broadcaster.subscribe('public')
    task = asyncio.create_task(send_room_msg(ws, subscriber))
    tasks.append(task)
    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await broadcaster.publish('public', msg.data)
                    # await ws.send_str(msg.data + '/answer')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('connection closed with exception %s' % ws.exception())
        return ws
    finally:
        for task in tasks:
            task.cancel()


async def send_room_msg(ws, subscriber):
    async for msg in subscriber:
        await ws.send_json({"message": msg})


app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('./'))

app.add_routes([
    web.get('/chat', chat_index),
    web.get('/chat/ws', chat_websocket),
])

if __name__ == '__main__':
    web.run_app(app)
