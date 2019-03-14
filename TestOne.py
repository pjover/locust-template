import datetime
import logging

import requests

from AbstractTest import AbstractTest
from Fields import Fields


class TestOne(AbstractTest):

    def __init__(self, test_url, fields, locust_mode, log_level=logging.INFO):
        super().__init__(
            test_url,
            "crud/arrivalDeparture/insert",
            "template_1.json",
            fields,
            locust_mode,
            log_level)

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


if __name__ == "__main__":
    test = TestOne(
            test_url="http://localhost:8085",
            fields=Fields(),
            locust_mode=False,
            log_level=logging.DEBUG)
    test.send(requests, "test")
