from locust import HttpLocust, TaskSet, task

from Fields import Fields
from TestOne import TestOne

ALL_FIELDS = Fields()


class TestOneTaskSet(TaskSet):

    # def __init__(self):
    #     super().__init__(self)
    test_one = TestOne(
        test_url="http://localhost:8085", #self.locust.host,
        fields=ALL_FIELDS,
        locust_mode=True)

    @task
    def send(self):
        self.test_one.send(self.client, "Test one")


class TestOneLocust(HttpLocust):
    host = "http://localhost:8085"
    task_set = TestOneTaskSet
    min_wait = 0
    max_wait = 1000
    weight = 100
