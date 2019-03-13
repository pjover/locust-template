from locust import HttpLocust, TaskSet, task

from Fields import Fields
from TestOne import TestOne

ENVIRONMENT = "LOCAL"
DEBUG_MODE = True
ALL_FIELDS = Fields({
    "adr_type",
    "boolean"
})


class TestOneTaskSet(TaskSet):
    test_one = TestOne(
        environment=ENVIRONMENT,
        fields=ALL_FIELDS,
        locust_mode=True,
        debug_mode=DEBUG_MODE)

    @task
    def send(self):
        self.test_one.send(self.client)


class TestOneLocust(HttpLocust):
    weight = 100
    task_set = TestOneTaskSet
    min_wait = 0
    max_wait = 1000
