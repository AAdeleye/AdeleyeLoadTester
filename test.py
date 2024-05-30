import time
from locust import HttpUser, task, between


class MyUser(HttpUser):
    wait_time = between(1, 3)  # Time between each task execution
    host = "http://httpbin.org/"
    @task
    def my_task(self):
        # Define the URL to test
        url = "http://httpbin.org/status/400%20%2C200"
        
        # Send an HTTP GET request
        response = self.client.get(url)
        
        # Print the response status code
        print(f"URL: {url} - Status Code: {response.status_code}")

    # If you want to specify the number of total requests and concurrent users:
    # total_requests = 100
    # total_clients = 10
    # tasks = [(MyUser, 1)]