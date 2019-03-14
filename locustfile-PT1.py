import logging

from locust import HttpLocust, TaskSet, task

from PerformanceTest import PerformanceTest
from Fields import Fields

ALL_FIELDS = Fields()


class PT1(PerformanceTest):

    def __init__(self, fields, log_level=logging.INFO):
        super().__init__(
            endpoint="crud/arrivalDeparture/insert",
            template_filename="template_1.json",
            fields=fields,
            log_level=log_level)

    def get_random_request(self):
        return self.get_template().render(
            createdOn=self.get_current_datetime(),
            lastUpdatedOn=self.get_current_datetime(),
            bookingPeriodFrom=self.get_random_date(0, 0),
            contractCode=self.get_random_int(1, 100000000),
            featureCode=self.get_random_string(2),
            id=self.get_random_int(1, 100000000),
            isOnRequest=self.get_random_boolean(),
            monday=self.get_random_boolean(),
            tuesday=self.get_random_boolean(),
            wednesday=self.get_random_boolean(),
            thursday=self.get_random_boolean(),
            friday=self.get_random_boolean(),
            saturday=self.get_random_boolean(),
            sunday=self.get_random_boolean(),
            lineNumber=self.get_random_int(1, 10),
            officeId=self.get_random_int(1, 100000),
            rateId=self.get_random_int(1, 100000),
            roomCode=self.get_random("Room.code"),
            travelWindowFrom=self.get_random_date(0, 10),
            travelWindowUntil=self.get_random_date(-10, 10),
            type=self.get_random("ArrivalDepartureRestriction.type")
        )


class PT1TaskSet(TaskSet):
    test_one = PT1(ALL_FIELDS)

    @task
    def send(self):
        self.test_one.send(
            name="Test one",
            locust=self.locust)


class PT1Locust(HttpLocust):
    host = "http://localhost:8085"
    task_set = PT1TaskSet
    min_wait = 0
    max_wait = 1000
    weight = 100


if __name__ == "__main__":
    test = PT1(Fields(), logging.DEBUG)
    test.send(
        name="Performance Test 1",
        locust=None,
        host="http://localhost:8085")
