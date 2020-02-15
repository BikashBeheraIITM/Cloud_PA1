import asyncio
from aiohttp import ClientSession
rate = 1000
async def fetch(url):
    async with ClientSession() as s, s.get(url) as res:
        ret = await res.read()
        return ret

async def print_when_done(tasks):
    i=0
    for res in asyncio.as_completed(tasks):
        print(await res)
        print("------------------------------------------------------------------------------------------------------------")
        print(i)
        i+=1

mil_req = [fetch("http://cloudpa1.us-east-1.elasticbeanstalk.com/") for i in range(rate)]

asyncio.run(print_when_done(mil_req))

