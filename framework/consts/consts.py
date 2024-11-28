import subprocess

TEST_SETUP_START_MESSAGE = "test setup - start"
TEST_SETUP_END_MESSAGE = "test setup - end"

TEST_TEARDOWN_START_MESSAGE = "test teardown - start"
TEST_TEARDOWN_END_MESSAGE = "test teardown - end"

SUITE_SETUP_START_MESSAGE = "suite setup - start"
SUITE_SETUP_END_MESSAGE = "suite setup - end"

SUITE_TEARDOWN_START_MESSAGE = "suite teardown - start"
SUITE_TEARDOWN_END_MESSAGE = "suite teardown - end"

SESSION_SETUP_START_MESSAGE = "session setup - start"
SESSION_SETUP_END_MESSAGE = "session setup - end"

SESSION_TEARDOWN_START_MESSAGE = "session teardown - start"
SESSION_TEARDOWN_END_MESSAGE = "session teardown - end"


class Defaults:
    """
    General default values
    """
    allure_server = "http://localhost:5050"
    process = subprocess.Popen("pwd", shell=True, stdout=subprocess.PIPE).stdout.read()
    pwd = process.decode("utf-8").strip()
    allure_dir = f"tests/allure-results"

