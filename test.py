import asyncio
async def my_coro(delay):
    loop = asyncio.get_running_loop()
    end_time = loop.time() + delay
    print(delay)
    while True:
        print("Blocking...")
        await asyncio.sleep(1)
        if loop.time() > end_time:
            print("Done.")
            break
async def main():
    await my_coro(6.0)
asyncio.run(my_coro(6.0))
asyncio.run(main())