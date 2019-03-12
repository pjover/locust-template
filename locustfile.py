from locust import HttpLocust, TaskSet, task

from TestOne import TestOne


class TestOneTaskSet(TaskSet):
    @task
    def run(self):
        test_runner = TestOne(
            environment="LOCAL",
            locust_mode=True,
            debug_mode=False)
        test_runner.run()


class TestOneLocust(HttpLocust):
    weight = 100
    task_set = TestOneTaskSet
    min_wait = 0
    max_wait = 1000
