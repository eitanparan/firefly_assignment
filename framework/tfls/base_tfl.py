import inspect
from retry.api import retry_call

import allure

from framework.infra.infra import Infra
from framework.logger.logger import Logger


class BaseTfl:
    """
    A class to represent a base TFL, all TFLs should inherit from this class
    """

    def __init__(self, infra=None, tfls=None, logger=None):
        from tfls.tfl import TFL
        self.tfls: TFL = tfls
        self.infra: Infra = infra
        self.logger_name = f'{self.__class__.__name__}'
        self.logger = logger if logger else Logger(self.logger_name).logger

    @staticmethod
    def step_wrapper(title="", error="", retries=1, delay=1):
        """
        A method for wrapping a test step (TFL). it handles the retrying, exception, and reporting
        :param title:
        :param error:
        :param retries:
        :param delay:
        :return:
        """

        def wrapper(func):
            @allure.step(title or func.__name__)
            def wrap(*args, **kwargs):
                try:
                    return retry_call(func, fargs=args, fkwargs=kwargs, tries=retries, delay=delay)
                except Exception as err:
                    if hasattr(args[0], 'logger'):
                        err = getattr(err, 'message', err)
                        args[0].logger.critical(f"Step Failure: step {func.__name__} {(error + ' --> ') or ''}"
                                                f" {err}")
                    if hasattr(args[0], 'infra'):
                        called_by_other_step = any("step_" in frame.function for frame in inspect.stack())
                    if kwargs.get('ignore_failure', None) is not True:
                        assert False, err
            return wrap
        return wrapper