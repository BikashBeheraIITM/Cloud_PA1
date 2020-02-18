import asyncio
from aiohttp import ClientSession
import time
import threading
from threading import Thread, current_thread, Lock
import numpy
import json

choice = int(input(
    "Choose Mode\n"+
    "1. Threads will restart immediately once they finish\n"+
    "2. All Threads will wait for execution completion of all threads and then restart\n"+
    "Enter Choice(1-2):"
))
aws = int(input(
    "Choose Back-end configuration:\n"+
    "1. Single Instance of Virtual Machine on AWS\n"+
    "2. 4 Instances of Virtual Machine on AWS with Load Balancer\n"+
    "3. Multiple Instances of Virtual Machine with Auto Scaling and Load Balancer\n"+
    "Enter choice(1-3):"
))
rate = int(input("Enter Requests per thread: "))
thread_count = int(input("Number of threads: "))

url_as = "http://cloudserverlb-76348161.us-east-1.elb.amazonaws.com/"
url_lb = "http://CloudLBv2-1284336746.us-east-1.elb.amazonaws.com/"
url_vm = "http://ec2-3-80-44-41.compute-1.amazonaws.com/"
url_local = "http://0.0.0.0:8080/"


class threaded_request_continuous(threading.Thread):
    def run(self):
        thread_req = {}
        thread_resp = {}
        thread_iter = {}
        
        f = open('threaded_request_continuous.txt', 'w') 
        while(True):
            s = time.monotonic_ns()
            mil_req = [send(url_as,i%100) for i in range(rate)]
            r = time.monotonic_ns() - s
            print(f"{current_thread().getName()} took {r/1000000.0:.3f} ms to send {rate} requests")
            try:
                asyncio.run(print_when_done(mil_req))
            except Exception as e:
                print(e)
                exit()
            e = time.monotonic_ns() - s
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
            print(f"{current_thread().getName()} received {rate} responses in {e/1000000.0:.3f} ms")
            ans = f"{current_thread().getName()} {rate} Requests\nRequest time: {r/1000000.0:.3f} ms\tResponse Time: {e/1000000.0:.3f} ms"
            f.write(ans)
            f.write("1\n")
            
class threaded_request_blocked(threading.Thread):
    def run(self):
        print(current_thread().getName()+"sent " + str(rate) + " requests")
        mil_req = [send(url_as,i%100) for i in range(rate)]
        try:
            asyncio.run(print_when_done(mil_req))
        except Exception as e:
            print(e)
            exit()
        print(current_thread().getName()+"finished " + str(rate) + " requests")


async def send(url,i):
    data = '?n='+str(i)
    async with ClientSession() as s, s.post(url+data) as res:
        return await s.close()
        #ret = await res.read()
        #return ret

async def print_when_done(tasks):
    for res in asyncio.as_completed(tasks):
        await res
try:
    if choice==1:
        thread_list = {threaded_request_continuous() for i in range(thread_count)}
        for thread in thread_list:
            thread.start()
    else:
        while True:
            thread_list = {threaded_request_blocked() for i in range(thread_count)}
            for thread in thread_list:
                thread.start()
            for t in threading.enumerate():
                try:
                    t.join()
                except RuntimeError as err:
                    pass

except KeyboardInterrupt as e:        
        pass        
    