# Locust 

Source : https://docs.locust.io/en/stable/installation.html

> pip install locust

create a file locustfile.py and copy the below contents

```python

from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("hello")
        
```
RUN :
> locust 


Open : http://localhost:8089/


To run specific file :
> locust -f my_locustfile.py

In gui host : http://localhost:8000/

Using cli :
locust --headless --users 10 --spawn-rate 1 -H http://127.0.0.1/

To run on distributed load :
https://docs.locust.io/en/stable/running-distributed.html#running-distributed