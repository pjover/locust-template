from locust import HttpLocust, TaskSet, task

from Fields import Fields
from TestOne import TestOne

ALL_FIELDS = Fields()


class TestOneTaskSet(TaskSet):
    test_one = TestOne(ALL_FIELDS)

    @task
    def send(self):
        self.test_one.send(
            name="Test one",
            locust=self.locust)


class TestOneLocust(HttpLocust):
    host = "http://localhost:8085"
    task_set = TestOneTaskSet
    min_wait = 0
    max_wait = 1000
    weight = 100
