import glob
import inspect
import os
import random
import sys


class Fields:
    __filenames_and_values = {}

    def __init__(self, location="field_lists/*.txt"):
        self.__load_files(location)

    def __load_files(self, location):
        path = "%s/%s" % (os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), location)
        for file in glob.glob(path):
            filename = os.path.splitext(os.path.basename(file))[0]
            self.__filenames_and_values[filename] = self.__load_file_content_as_list(file)

    @staticmethod
    def __decode_line(line):
        return line.rstrip('\n\r')

    def __load_file_content_as_list(self, file):
        try:
            file_content_as_list = [self.__decode_line(line) for line in open(file)]
        except FileNotFoundError:
            sys.exit("Field list file '%s' not found" % file)
        return file_content_as_list

    def get_all(self, field):
        return self.__filenames_and_values[field]

    def get_random(self, field):
        list_of_values = self.get_all(field)
        return list_of_values[random.randint(0, len(list_of_values) - 1)]


if __name__ == "__main__":
    test = Fields()
    print(test.get_all("ArrivalDepartureRestriction.type"))
    print(test.get_random("ArrivalDepartureRestriction.type"))
    print(test.get_all("Room.code"))
    print(test.get_random("Room.code"))
