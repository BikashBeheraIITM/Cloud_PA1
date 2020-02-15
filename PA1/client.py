import asyncio
from aiohttp import ClientSession
rate = 10
async def send(url,data):
    async with ClientSession() as s, s.post(url,data = data) as res:
        ret = await res.read()
        resp = ret.json()
        print(resp)

async def print_when_done(tasks):
    for res in asyncio.as_completed(tasks):
        print(await res)

mil_req = [send("localhost:8080/",i) for i in range(rate)]

asyncio.run(print_when_done(mil_req))

