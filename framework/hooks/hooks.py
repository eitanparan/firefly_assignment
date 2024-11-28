from datetime import datetime
from framework.consts.consts import Defaults as defaults

def pytest_addoption(parser):
    """
    handling pytest command line arguments
    :param parser:
    :return:
    """
    _time = datetime.now().strftime('%Y-%m-%d--%H-%M-%S')

    parser.addoption("--report_identifier", action="store", default=_time, help="report unique name")
    parser.addoption("--allure_server", action="store", default=defaults.allure_server, help="allure server address")
    parser.addoption("--clean_allure_history", action="store", default=True, help="allure server address")
    parser.addoption("--log_level", action="store", default=None, help="log level")
    parser.addoption("--verbose_logs", action="store", default=False, help="show verbose logs")
