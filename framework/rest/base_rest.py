import requests
from requests.auth import HTTPBasicAuth
from framework.logger.logger import Logger
from framework.general.general import General


class BaseRest:
    """
    A class for representing the Base class for REST client
    """

    def __init__(self):
        logger_name = f'Rest{self.__class__.__name__}'
        self.logger = Logger(logger_name=logger_name).logger
        self.base_url = "http://localhost:8080/api/v1"
        self.auth = None
        self.headers = {"accept": "application/json", "Content-Type": "application/json"}
        self.general = General()


    def get(self, url=None, headers=None, payload=None, auth=None, **kwargs):
        """
        A method for wrapping request.get method and logging all informative data about the request
        :return: REST http response
        """
        try:
            response = requests.get(url=f'{url}', headers=headers, json=payload, auth=auth, timeout=30, **kwargs)
            self.preety_log(logger=self.logger, url=url, data=payload, response=response)
            return response
        except Exception as err:
            raise Exception(f"Failed executing REST get for url: {url}, headers: {headers}, payload: {payload}: {err}")


    def post(self, url=None, headers=None, payload=None, auth=None, **kwargs):
        """
        A method for wrapping request.post method and logging all informative data about the request
        :return: REST http response
        """
        try:
            response = requests.post(url=url, headers=headers, auth=auth, json=payload, timeout=30, **kwargs)
            self.preety_log(logger=self.logger, url=url, data=payload, response=response)
            return response
        except Exception as err:
            raise Exception(f"Failed executing REST post for url: {url}, headers: {headers}, payload: {payload}: {err}")


    def put(self, url=None, headers=None, payload=None, auth=None, **kwargs):
        """
        A method for wrapping request.put method and logging all informative data about the request
        :return: REST http response
        """
        try:
            response = requests.put(url=url, headers=headers, auth=auth, json=payload, timeout=30, **kwargs)
            self.preety_log(logger=self.logger, url=url, data=payload, response=response)
            return response
        except Exception as err:
            raise Exception(f"Failed executing REST put for url: {url}, headers: {headers}, payload: {payload}: {err}")


    def patch(self, url=None, headers=None, payload=None, auth=None, **kwargs):
        """
        A method for wrapping request.patch method and logging all informative data about the request
        :return: REST http response
        """
        try:
            response = requests.patch(url=url, headers=headers, auth=auth, json=payload, timeout=30, **kwargs)
            self.preety_log(logger=self.logger, url=url, data=payload, response=response)
            return response
        except Exception as err:
            raise Exception(f"Failed executing REST patch for url: {url}, headers: {headers}, payload: {payload}: {err}")


    def delete(self, url=None, headers=None, payload=None, auth=None, **kwargs):
        """
        A method for wrapping request.delete method and logging all informative data about the request
        :return: REST http response
        """
        try:
            response = requests.delete(url=url, headers=headers, auth=auth, timeout=30)
            self.preety_log(logger=self.logger, url=url, response=response)
            return response
        except Exception as err:
            raise Exception(f"Failed executing REST delete for url: {url}, headers: {headers}, payload: {payload}: "
                            f"{err}")

    def authentication(self, user=None, password=None):
        """

        :param user:
        :param password:
        :return:
        """
        try:
            auth = HTTPBasicAuth(user, password)
            return auth
        except Exception as err:
            raise Exception(f"Failed to get authentication object: {err}")


    def preety_log(self, logger: Logger = None, url=None, headers=None, data=None, response=None):
        """

        :param url:
        :param headers:
        :param data:
        :param response:
        :return:
        """
        try:
            logger = logger or self.logger
            logger.debug(f"Url: {url}")
            logger.debug(f"Headers: {headers}")
            logger.debug(f"Data: {data}")
            logger.debug(f"Status code: {response.status_code}")
            logger.debug(f"Content: {response.content}")
        except Exception as err:
            logger.warning(f"Failed to print log: {err}")


    @classmethod
    def static_preety_log(cls, logger: Logger = None, url=None, headers=None, data=None, response=None):
        """

        :param url:
        :param headers:
        :param data:
        :param response:
        :return:
        """
        try:
            _logger = logger
            _logger.logger.debug(f"Url: {url}")
            _logger.logger.debug(f"Headers: {headers}")
            if data:
                _logger.logger.debug(f"Data: {data}")
            _logger.logger.debug(f"Status code: {response.status_code}")
            _logger.logger.debug(f"Content: {response.content}")
        except Exception as err:
            _logger.logger.warning(f"Failed to print log: {err}")

class RdoObject:
    """
    A class for representing a general Rest Data Object
    """

    def __init__(self, headers, url, **kwargs):
        self.headers = headers
        self.url = url
        self.__dict__.update(kwargs)
