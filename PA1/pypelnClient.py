from aiohttp import ClientSession, TCPConnector
import asyncio
import sys
from pypeln import asyncio_task as aio
import random

limit = int(input("Enter Rate of Requests per second: "))
url = "http://cloudserverlb-76348161.us-east-1.elb.amazonaws.com/"
u = [url for i in range(limit)]
random.seed()

async def send(url,session):
    i = random.randint(1,101)
    data = '?n='+str(i)
    print(data)
    async with session.post(url+data) as res:
        return await res.read()

while True:    
    aio.each(
        send, 
        u,
        workers = limit,
        on_start = lambda: ClientSession(connector=TCPConnector(limit=None)),
        on_done = lambda _status, session: session.close(),
        run = True,
    )