import datetime
import inspect
import os
import random
from abc import abstractmethod

import jinja2


class AbstractTest:
    __TEMPLATE_PATH = "%s/templates/" % os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    __LOG_FILENAME = "log.txt"
    __URL_PREFIX = "/"
    __HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}
    __TIMEOUT = 60.0  # seconds
    __VERIFY = False
    __BUFFER_MAX_SIZE = 1000

    def __init__(self, environment, endpoint, template_filename, fields, locust_mode, debug_mode):
        self.__init_test_host(environment)
        self.init_logs(environment)
        self.__endpoint = endpoint
        self.template_filename = template_filename
        self.__fields = fields
        self.__locust_mode = locust_mode
        self.__debug_mode = debug_mode
        self.__init_jinja()
        self.debug("Working with host '%s'" % self.__test_host)

    def __init_test_host(self, environment):
        if environment == "LOCAL":
            self.__test_host = "http://localhost:8085"
        elif environment == "DEV":
            self.__test_host = "http://hotel-contract-service.dev-hbg-aws-eu-west-1.service"
        elif environment == "TEST":
            self.__test_host = "http://hotel-contract-service.test-hbg-aws-eu-west-1.service"
        else:
            raise ValueError("Invalid environment, should be `LOCAL`, `DEV` or `TEST`")

    def init_logs(self, environment):
        open(self.__LOG_FILENAME, "w") \
            .write("%s (%s environment)\n\n" % (str(datetime.datetime.now()), environment))

    def debug(self, log_to_print):
        if self.__debug_mode:
            print(log_to_print)

    def __init_jinja(self):
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.__TEMPLATE_PATH),
            trim_blocks=True,
            lstrip_blocks=True)
        self.__template = env.get_template(self.template_filename)

    def get_template(self):
        return self.__template

    @abstractmethod
    def get_random_request(self):
        raise NotImplementedError()

    def get_random(self, field):
        return self.__fields.get_random(field)

    def send(self, request, body=None):
        if not body:
            body = self.get_random_request()
        if self.__locust_mode:
            response = request.request(
                url=self.__get_url(self.__endpoint),
                name=self.__endpoint,
                method="POST",
                headers=self.__HEADERS,
                data=body,
                timeout=self.__TIMEOUT,
                verify=self.__VERIFY)
        else:
            response = request.request(
                url=self.__get_url(self.__endpoint),
                method="POST",
                headers=self.__HEADERS,
                data=body,
                timeout=self.__TIMEOUT,
                verify=self.__VERIFY)
        if self.__is_error(response):
            self.__log_error("POST (%s): %s" % (self.__endpoint, body), response)
            return None
        return response

    def __get_url(self, *endpoint_name_parts):
        suffix = "/".join(endpoint_name_parts)
        if self.__locust_mode:
            # Locust will add the server address to the url
            url = self.__URL_PREFIX + suffix
        else:
            # At test mode (without locust) adds the server address to the url
            url = self.__test_host + self.__URL_PREFIX + suffix
        self.debug("URL: %s" % url)
        return url

    @staticmethod
    def __is_error(response):
        return response.status_code != 200

    def __log_error(self, request, response):
        log_txt = "Input: %s\nResponse status: %s\nResponse: %s" % (request, response.status_code, response.text)
        self.debug(log_txt)
        try:
            with open(self.__LOG_FILENAME, "a") as f:
                f.write(log_txt)
        except ValueError:
            pass

    @staticmethod
    def get_random_date(days_before_today, days_after_today):
        period_start = datetime.datetime.today() - datetime.timedelta(days=days_before_today)
        random_days = random.randint(0, days_before_today + days_after_today)
        random_date = period_start + datetime.timedelta(days=random_days)
        return random_date.strftime('%Y-%m-%d')
