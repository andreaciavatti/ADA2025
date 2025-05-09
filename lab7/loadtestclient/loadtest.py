from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(1, 2)
    
    @task
    def index(self):
        self.client.get("http://34.122.202.24:8080/ordersinventories/Laptop/id1")     
