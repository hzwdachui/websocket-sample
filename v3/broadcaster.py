import asyncio


class Broadcaster:
    """广播工具类-用于封装房间消息传递功能
    当前采用内存实现，实际上可以用 Redis、RabbitMQ 来实现
    """

    def __init__(self):
        self.channels = dict()

    async def publish(self, channel, msg):
        """发布消息到指定频道
        """
        for queue in self.channels.get(channel, []):
            await queue.put(msg)

    async def subscribe(self, channel):
        """订阅指定频道的消息
        """
        queue = asyncio.Queue()
        if channel not in self.channels:
            self.channels.setdefault(channel, [])
        self.channels[channel].append(queue)
        await queue.put('initialized')
        return Subscriber(queue)

    async def unsubscribe(self, channel):
        pass


class Subscriber:
    """消息订阅类-用于接收消息
    """

    def __init__(self, queue):
        self.queue = queue

    async def __aiter__(self):
        while True:
            yield await self.queue.get()
            self.queue.task_done()
