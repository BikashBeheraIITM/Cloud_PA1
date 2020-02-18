import asyncio
from aiohttp import ClientSession
import time
rate = int(input("No of requests to be sent at once: "))

async def send(url,i):
    data = '?n='+str(i)
    async with ClientSession() as s, s.post(url+data) as res:
        #ret = await res.read()
        return await s.close()
        #return ret

async def print_when_done(tasks):
    for res in asyncio.as_completed(tasks):
        await res
        

url_aws = "http://cloudserverlb-76348161.us-east-1.elb.amazonaws.com/"
url_local = "http://0.0.0.0:8080/"

while True:
    START = time.monotonic()
    mil_req = [send(url_aws,i%100) for i in range(rate)]
    req = time.monotonic() - START
    print(f"Time to send {rate} requests: ",req)
    try:
        asyncio.run(print_when_done(mil_req))
    except Exception as e:
        print(e)
        exit()
    now = time.monotonic() - START
    print(f"Response time to process {rate} requests: ",now)