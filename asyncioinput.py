from concurrent.futures.thread import ThreadPoolExecutor
# https://docs.python.org/zh-cn/3/library/functools.html#functools.partial
from functools import partial
import asyncio


def always_input():
    while True:
        text = input("please input")
        print("input text: " + text)


async def async_input():
    await asyncio.get_running_loop().run_in_executor(
        ThreadPoolExecutor(1),
        always_input
    )


async def async_print():
    while True:
        await asyncio.sleep(2)
        print("I'm printing")


async def main():
    task1 = asyncio.create_task(async_input())
    task2 = asyncio.create_task(async_print())
    await task1
    await task2

asyncio.run(main())
