import datetime
import inspect
import logging
import os
import random
import string
from abc import abstractmethod

import jinja2
import requests

HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}
TIMEOUT = 60.0  # seconds
VERIFY = False


class PerformanceTest:
    __TEMPLATE_PATH = "%s/templates/" % os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    __LOG_FILENAME = "log.txt"
    __URL_PREFIX = "/"
    __BUFFER_MAX_SIZE = 1000
    __RANDOM_CHARS_SEED = string.ascii_uppercase + string.digits
    __LOGGING_FORMAT = '%(asctime)-15s %(message)s'

    def __init__(self, endpoint, template_filename, fields, log_level):
        self.__endpoint = endpoint
        self.template_filename = template_filename
        self.__fields = fields

        self.__logger = self.init_logging(log_level)
        self.__init_jinja()
        self.__logger.info("Started endpoint:'%s' template:'%s'", endpoint, template_filename)

    def init_logging(self, log_level):
        logging.basicConfig(format=self.__LOGGING_FORMAT)
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(log_level)
        return logger

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

    def send(self, name, locust, host=None, body=None):
        if not body:
            body = self.get_random_request()
        if locust:
            url = self.__get_url()
            response = self.__send_with_locust(name, locust, url, body)
        else:
            if not host:
                raise ValueError("host must be defined if locust is None")
            url = self.__get_url(host)
            response = self.__send_without_locust(url, body)

        if self.__is_error(response):
            self.__logger.error("POST to URL: %s\nRequest: %s\nResponse status code: %s\nResponse text: %s",
                                url, body, response.status_code, response.text)
        else:
            self.__logger.debug(response.text)

        return response

    def __get_url(self, host=None):
        suffix = self.__get_url_suffix(self.__endpoint)
        if host:
            url = host + suffix
        else:
            url = suffix
        self.__logger.debug("URL: %s", url)
        return url

    def __get_url_suffix(self, *endpoint_name_parts):
        suffix = "/".join(endpoint_name_parts)
        return self.__URL_PREFIX + suffix

    def __send_with_locust(self, name, locust, url, body):
        return locust.client.request(
            url=url,
            name=name,
            method="POST",
            headers=HEADERS,
            data=body,
            timeout=TIMEOUT,
            verify=VERIFY)

    def __send_without_locust(self, url, body):
        return requests.request(
            url=url,
            method="POST",
            headers=HEADERS,
            data=body,
            timeout=TIMEOUT,
            verify=VERIFY)

    @staticmethod
    def __is_error(response):
        return response.status_code != 200

    @staticmethod
    def get_random_int(low, high):
        return random.randint(low, high)

    @staticmethod
    def get_random_boolean():
        return str(bool(random.getrandbits(1))).lower()

    def get_random_string(self, size):
        return ''.join(random.choice(self.__RANDOM_CHARS_SEED) for _ in range(size))

    @staticmethod
    def get_random_date(days_before_today, days_after_today):
        period_start = datetime.datetime.today() - datetime.timedelta(days=days_before_today)
        random_days = random.randint(0, days_before_today + days_after_today)
        random_date = period_start + datetime.timedelta(days=random_days)
        return random_date.strftime('%Y-%m-%d')

    @staticmethod
    def get_current_datetime():
        return datetime.datetime.now().isoformat()
