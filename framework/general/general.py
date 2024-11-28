import os
import sys
import logging

import json

from framework.general import lists, files, string_helper


class General:
    """
    A class for holding all modules under general folder
    """

    def __init__(self):
        self.files = files
        self.lists = lists
        self.string_helper = string_helper

    def delete_file(self, path):
        """

        :param path:
        :return:
        """
        try:
            print(path)
            os.remove(path)
        except OSError:
            pass

    @staticmethod
    def parse_command_line_args():
        """

        :return:
        """
        try:
            raw_args = sys.argv
            args = {}
            for index in range(len(raw_args)):
                if '-' in str(raw_args[index][0]):
                    if '-' not in str(raw_args[index + 1][0]):
                        args[str(raw_args[index]).lstrip('-')] = raw_args[index + 1]
            return args
        except Exception as err:
            raise Exception(f"Failed to parse command line arguments: {err}")

    def json_to_python_object(self, _json):
        """
        for example, json can be json = '{"name": "John Smith", "hometown": {"name": "New York", "id": 123}}'
        """
        try:

            json_to_object = DictObject.from_dict(_json)
            return json_to_object
        except Exception as err:
            raise Exception(f"failed to convert json to python object. json = {_json}: {err}")


    @staticmethod
    def check_if_logger_exist(logger_name):
        """

        """
        try:
            loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
            if logger_name in loggers:
                return True
            return False
        except Exception:
            return False


class DictObject(object):
    """
    For converting a dict to a dict object
    """

    def __init__(self, dict_):
        self.__dict__.update(dict_)

    @classmethod
    def from_dict(cls, d):
        return json.loads(json.dumps(d), object_hook=DictObject)
