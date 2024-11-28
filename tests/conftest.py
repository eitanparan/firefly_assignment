import os
import sys

import pytest

from framework.infra.infra import Infra
from framework.logger.logger import Logger
from tfls.tfl import TFL as _TFL
from framework.reporting.allure_report import AllureReport
from framework.session.session import BaseSession

sys.path.append(os.getcwd())

# Importing hooks as plugins. the most important hook is the pytest_addoption for enabling custom command line arguments
# passed to pytest

pytest_plugins = ["framework.hooks"]

collect_ignore = ["data.py"]
logger = Logger('conftest').logger

# Instantiating meta (Global) objects
infra_instance = None
tfl_instance = None
allure_obj = None
session_obj = None


# ############################################### Fixtures ########################################################

@pytest.fixture(scope="session", autouse=True)
def infra(request):
    """
    A fixture for initializing the object representing the infrastructure/framework layer
    :return: None
    """
    global infra_instance
    logger.info('Instantiating infra fixture')
    infra_instance = Infra()
    yield infra_instance


@pytest.fixture(scope="session", autouse=True)
def TFL(request, infra):
    """
    A fixture for initializing the object representing the TFL (tests steps) layer
    :return: None
    """
    global tfl_instance
    logger.info('Instantiating TFL fixture')
    tfl_instance = _TFL(infra=infra)
    yield tfl_instance


@pytest.fixture(scope="session", autouse=True)
def allure(request, infra, TFL):
    """
    A fixture for initializing the object responsible for allure (reports)
    :return: None
    """
    global allure_obj
    logger.info('Instantiating allure fixture')
    allure_obj = allure_obj if allure_obj else AllureReport(infra=infra)
    yield allure_obj


@pytest.fixture(scope="session", autouse=True)
def session_instance(request, infra, TFL, allure):
    """
    A fixture for initializing the object representing the pytest session
    :return: None
    """
    global session_obj
    logger.info('Instantiating session_instance fixture')
    session_obj = BaseSession(infra=infra, allure_obj=allure, request=request)
    yield session_obj


@pytest.fixture(scope="session", autouse=True)
def session_setup(request, allure, infra, TFL, session_instance):
    """
    A fixture for executing the session setup
    :return: None
    """
    session_instance.setup()
    yield


@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_sessionfinish(session):
    """
    sessionfinish / teardown operations, such as creating a report
    :return: None
    """
    global session_obj
    global env_instance
    yield
    try:
        Logger('conftest').logger.info("calling session teardown")
        session_obj.teardown()
    except Exception as err:
        err_msg = f"session teardown failed. reason: {err}"
        Logger('conftest').logger.critical(err_msg)
    return
