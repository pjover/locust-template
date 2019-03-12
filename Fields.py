import datetime
import inspect
import os
import random
import sys


class Fields:
    __FIELD_LISTS_PATH = "%s/field_lists/" % os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    __filenames_and_values = {}

    def __init__(self, filenames):
        self.filenames = filenames
        self.__load_files()

    def __load_files(self):
        for filename in self.filenames:
            self.__filenames_and_values[filename] = self.__load_file_content_as_list(filename + ".txt")

    @staticmethod
    def __decode_line(line):
        return line.rstrip('\n\r')

    def __get_file_path(self, filename):
        return os.path.join(self.__FIELD_LISTS_PATH, filename)

    def __load_file_content_as_list(self, filename):
        try:
            file_content_as_list = [self.__decode_line(line) for line in open(self.__get_file_path(filename))]
        except FileNotFoundError:
            sys.exit("Field list file '%s' not found" % self.__get_file_path(filename))
        return file_content_as_list

    def get_all(self, field):
        return self.__filenames_and_values[field]

    def get_random(self, field):
        list_of_values = self.get_all(field)
        return list_of_values[random.randint(0, len(list_of_values) - 1)]


if __name__ == "__main__":
    test = Fields({
        "adr_type",
        "boolean"
    })
    print(test.get_all("adr_type"))
    print(test.get_random("adr_type"))
    print(test.get_all("boolean"))
    print(test.get_random("boolean"))
    print(Fields.get_random_date(10, 10))
