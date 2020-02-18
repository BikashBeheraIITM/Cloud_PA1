from aiohttp import ClientSession, TCPConnector
import asyncio
import sys
from pypeln import TaskPool
import random 

limit = int(input("Enter Rate of Requests per second: "))

async def send(url, session):
    i = random.randint(1,101)
    data = '?n='+str(i)
    async with session.post(url+data) as response:
        return await response.read()

async def main(url):
    connector = TCPConnector(limit=None)
    i = 0
    req_cnt = 0
    async with ClientSession(connector=connector) as session, TaskPool(limit,loop) as tasks:
        while True:
            i+=1
            if i%1000==0:
                req_cnt+=1
            await tasks.put(send(url, session))
            


url = "http://cloudserverlb-76348161.us-east-1.elb.amazonaws.com/"
loop = asyncio.get_event_loop()
loop.run_until_complete(main(url))