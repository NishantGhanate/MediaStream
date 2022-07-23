from locust import HttpUser, task, tag

class HelloWorldUser(HttpUser):

    def on_start(self):
        # Test a demo page
        self.client.get("")

    
    @tag('world-content')    
    @task
    def watch_world(self):
        self.client.get("watch/the-world")

    # @task(3)
    # def search(self):
    #     response = self.client.get("watch/content?title={}")
    #     print("Response status code:", response.status_code)
    #     print("Response text:", response.text)

        