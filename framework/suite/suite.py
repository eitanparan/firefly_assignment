import time
import retry

from framework.general import files
from framework.infra.infra import Infra
from framework.logger.logger import Logger
from tfls.tfl import TFL as _TFL


class BaseSuite:
    """
    A class for representing a suite. mainly to be used in conftest fixture for calling suite setup and teardown
    """

    def __init__(self, infra: Infra=None, tfl: _TFL=None, request=None, ):
        self.infra: Infra = infra
        self.tfl = tfl
        self.request = request
        self.suite_name = self.request.node.name
        self.logger_name = f'{self.suite_name}'
        self.logger = Logger(self.suite_name).logger

    def setup(self, request=None, infra: Infra = None, TFL: _TFL = None):
        """

        :return:
        """
        try:
            self.allign_logs()
            self.logger.warning(f"{'*' * 10} Execution of SUITE SETUP for{self.suite_name} is starting {'*' * 10}")

            private_setup = getattr(request.cls, 'suite_setup', None)
            if private_setup:
                self.logger.notification(f"starting private setup for suite {self.suite_name}")
                parametrize_values = getattr(request.node.callspec, 'params',
                                             None) if getattr(request.node, 'callspec', None) else None
                private_setup(request.cls, infra=infra, TFL=TFL, parametrize_values=parametrize_values)
                self.logger.notification(f"private setup ended for suite {self.suite_name}")

            self.logger.warning(f"{'*' * 10} Execution of SUITE SETUP for{self.suite_name} has ended {'*' * 10}")
        except Exception as err:
            self.teardown(request=request, infra=self.infra, TFL=TFL)
            self.logger.critical(f"Suite setup failed. skipping suite: {err}")
            raise Exception(f"Suite setup failed. skipping suite: {err}")


    def teardown(self, request=None, infra: Infra = None, TFL: _TFL = None):
        """

        :return:
        """
        try:
            self.allign_logs()
            self.logger.warning(f"{'*' * 10} Execution of SUITE TEARDOWN for{self.suite_name} is starting {'*' * 10}")

            private_teardown = getattr(request.cls, 'suite_teardown', None)
            if private_teardown:
                self.logger.notification(f"starting private teardown for suite {self.suite_name}")
                parametrize_values = getattr(request.node.callspec, 'params', None) if getattr(request.node, 'callspec',
                                                                                               None) else None
                private_teardown(request.cls, infra=infra, TFL=TFL, parametrize_values=parametrize_values)
                self.logger.notification(f"private teardown ended for suite {self.suite_name}")

            self.logger.warning(f"{'*' * 10} Execution of SUITE TEARDOWN for{self.suite_name} has ended {'*' * 10}")
        except Exception as err:
            self.logger.critical(f"Suite teardown failed: {err}")
            raise Exception(f"Suite teardown failed: {err}")


    def allign_logs(self):
        """

        :return:
        """
        print('\n')