import requests

from AbstractTest import AbstractTest
from Fields import Fields


class TestOne(AbstractTest):

    def __init__(self, environment, locust_mode, debug_mode):
        super().__init__(
            environment,
            "crud/arrivalDeparture/insert",
            "template_1.json",
            Fields({
                "adr_type",
                "boolean"
            }),
            locust_mode,
            debug_mode)

    def get_random_request(self):
        return self.get_template().render(
            createdOn=self.get_random_date(0, 0),
            lastUpdatedOn=self.get_random_date(0, 0),
            monday=self.get_random("boolean"),
            tuesday=self.get_random("boolean"),
            wednesday=self.get_random("boolean"),
            thursday=self.get_random("boolean"),
            friday=self.get_random("boolean"),
            saturday=self.get_random("boolean"),
            sunday=self.get_random("boolean"),
            type=self.get_random("adr_type")
        )


if __name__ == "__main__":
    test = TestOne(
            environment="LOCAL",
            locust_mode=False,
            debug_mode=True)
    test.send(requests)
