from locust import HttpLocust, TaskSet, task, between
from locust.contrib.fasthttp import FastHttpLocust
import random
class WebsiteTasks(TaskSet):
    def on_start(self):
        self.client.get("/")
    
    @task
    def send(self):
        random.seed(5)
        n = random.randint(1,1000)
        self.client.post("/?n="+str(n))

class WebsiteUser(FastHttpLocust):
    task_set = WebsiteTasks
    wait_time = between(1, 1)