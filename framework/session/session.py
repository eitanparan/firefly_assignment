
from framework.reporting.allure_report import AllureReport
from framework.logger.logger import Logger
from framework.infra.infra import Infra


class BaseSession:
    """
    A class for representing a pytest session. mainly to be used in conftest fixture for calling seesion setup and
    teardown
    """

    def __init__(self, infra=None, allure_obj=None, request=None):
        self.request = request
        self.infra: Infra = infra
        self.suite_name = self.get_suite_name()
        self.allure_obj: AllureReport = allure_obj
        self.logger = Logger('Session').logger
        self.logger.info("BaseSession was initialized successfully")

    def setup(self):
        """

        :return:
        """
        try:
            self.allign_logs()
            self.logger.warning(f"{'*' * 30} Execution of SESSION SETUP is starting {'*' * 30}")
            self.allure_obj.delete_allure_results_dir_content(allure_results_directory=self.allure_obj.allure_dir)
            self.logger.warning(f"{'*' * 30} Execution of SESSION SETUP has ended {'*' * 30}")
        except Exception as err:
            raise Exception(err)

    def teardown(self):
        """

        :return:
        """
        try:
            self.allign_logs()
            self.logger.warning(f"{'*' * 30} Execution of SESSION TEARDOWN is starting {'*' * 30}")
            self.allure_obj.send_results(allure_server=self.allure_obj.allure_server,
                                         allure_results_directory=self.allure_obj.allure_dir,
                                         project_id=self.allure_obj.project_id, create_project=True)
            self.allure_obj.generate_latest_report_link(project_id=self.allure_obj.project_id)
            self.logger.warning(f"{'*' * 30} Execution of SESSION TEARDOWN has ended {'*' * 30}")
        except Exception as err:
            raise Exception(f"Session teardown failed: {err}")

    def allign_logs(self):
        """

        :return:
        """
        print('\n')

    def get_suite_name(self):
        """
        Gets the name of the suite from the request fixture
        :return: str representing the name of the suite in camel case as it is written in the suite module, for example
                 TestSuiteSanity
        """
        try:
            node = getattr(self.request, 'node', None)
            items = getattr(node, 'items', None)
            first_test = items[0] if (type(items) is list and len(items) > 0) else None
            suite_object = getattr(first_test, 'parent', None)
            suite_name = getattr(suite_object, 'name', None) or ''
            return suite_name
        except Exception:
            self.logger.debug(f"no suite found in request fixture, setting suite name to empty string")
            return ''
