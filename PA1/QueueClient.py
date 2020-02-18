import asyncio
from aiohttp import ClientSession
import time
import threading
from threading import Thread, current_thread, Lock
import numpy
from queue import Queue
import random

aws = int(input(
    "Choose Back-end configuration:\n"+
    "1. Single Instance of Virtual Machine on AWS\n"+
    "2. 2 Instances of Virtual Machine on AWS with Load Balancer\n"+
    "3. Multiple Instances of Virtual Machine with Auto Scaling and Load Balancer\n"+
    "Enter choice(1-3):"
))

url_as = "http://cloudserverlb-76348161.us-east-1.elb.amazonaws.com/"
url_lb = "http://CloudLBv2-1284336746.us-east-1.elb.amazonaws.com/"
url_vm = "http://ec2-3-80-44-41.compute-1.amazonaws.com/"
url_local = "http://0.0.0.0:8080/"

if aws==1:
    url = url_vm
elif aws==2:
    url = url_lb
elif aws==3:
    url = url_as
else:
    print("Wrong Input")
    exit()
    
rate = int(input("Enter Requests per thread: "))
thread_count = int(input("Number of threads: "))

thread_queue = Queue(maxsize=1000_000_000_000)
#f = open('threaded_request_continuous.txt', 'w') 

def thread_send(t,q):
    #thread_req = {}
    #thread_resp = {}
    #thread_iter = {}
    
    while True:
        s = time.monotonic_ns()
        url = q.get()
        mil_req = [send(url) for i in range(rate)]
        r = time.monotonic_ns() - s
        print(f"{current_thread().getName()} took {r/1000000.0:.3f} ms to send {rate} requests")
        asyncio.run(print_when_done(mil_req))
        e = time.monotonic_ns() - s
        '''
        if current_thread().getName() in thread_iter.keys():
            count = thread_iter[current_thread().getName()]
            prev_req = thread_req[current_thread().getName()]
            avg_req = (prev_req*count+r)/(count+1)
            prev_resp = thread_resp[current_thread().getName()]
            avg_resp = (prev_resp*count+e)/(count+1)
            thread_req[current_thread().getName()] = avg_req
            thread_resp[current_thread().getName()] = avg_resp
        else:
            thread_iter[current_thread().getName()] = 1
            thread_req[current_thread().getName()] = r
            thread_resp[current_thread().getName()] = e
        '''
        print(f"{current_thread().getName()} received {rate} responses in {e/1000000.0:.3f} ms")
        ans = f"{current_thread().getName()} {rate} Requests\nRequest time: {r/1000000.0:.3f} ms\tResponse Time: {e/1000000.0:.3f} ms"
        q.task_done()

async def send(url):
    async with ClientSession() as s, s.post(url) as res:
        return await s.close()
        #ret = await res.read()
        #return ret

async def print_when_done(tasks):
    i = 0
    for res in asyncio.as_completed(tasks):
        i+=1
        if(i%100==0):
            print(f"hundred responses received: {i}")
        await res

for t in range(thread_count):
    worker = Thread(target=thread_send, args=(t,thread_queue,),daemon=True)
    worker.start()

try:
    random.seed()
    start_time = time.monotonic_ns()/1000000000.0
    elapsed_time = 0
    for a in range(100000):
        i = random.randint(1,101)
        data = '?n='+str(i)
        thread_queue.put(url+data)
        elapsed_time = (time.monotonic_ns()/1000000000.0) - start_time
        #if elapsed_time >30:
        #    exit()
    thread_queue.join()
except KeyboardInterrupt as e:        
        pass        
    