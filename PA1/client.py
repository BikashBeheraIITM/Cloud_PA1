import asyncio
from aiohttp import ClientSession
rate = 10000
async def send(url,i):
    data = '?n='+str(i)
    async with ClientSession() as s, s.post(url+data) as res:
        ret = await res.read()
        return ret

async def print_when_done(tasks):
    for res in asyncio.as_completed(tasks):
        await res

mil_req = [send("http://localhost:8080/",i) for i in range(rate)]

asyncio.run(print_when_done(mil_req))

