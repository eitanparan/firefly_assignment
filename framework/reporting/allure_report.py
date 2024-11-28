import base64
import json
import os
import shutil

import requests
import retry
from datetime import datetime

from framework.general import files as _files
from framework.logger.logger import Logger
from framework.consts.consts import Defaults as defaults


class AllureReport:
    """
    A class for handling all of the allure calls, including handling files, reports ect...
    """

    def __init__(self, infra=None):
        """

        :param infra:
        """
        self._time = datetime.now().strftime('%Y-%m-%d--%H-%M-%S')
        self.logger = Logger(logger_name='AllureReport').logger
        self.infra = infra
        self.allure_server = defaults.allure_server
        self.project_id = self._time
        self.allure_dir = defaults.allure_dir
        self.report_link = (f'{self.allure_server}/allure-docker-service/projects/{self.project_id}/reports/latest/'
                            f'index.html')

    def get_all_files_for_report(self, allure_results_directory=None):
        """

        :return:
        """
        try:
            _files.wait_for_file_to_exist(directory=allure_results_directory, file_name_contains='result.json')
            self.logger.debug("Getting all files to report - allure")
            results_directory = allure_results_directory
            files = os.listdir(results_directory)
            results = []
            for file in files:
                result = {}
                file_path = results_directory + "/" + file
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, "rb") as f:
                            content = f.read()
                            if content.strip():
                                b64_content = base64.b64encode(content)
                                result['file_name'] = file
                                result['content_base64'] = b64_content.decode('UTF-8')
                                results.append(result)
                    finally:
                        f.close()
            return results
        except Exception as err:
            self.logger.error(f"Failed to get all files for report: {err}")
            raise ValueError(err)

    def send_results(self, allure_results_directory=None, allure_server=None, project_id=None, create_project=False):
        """

        :return:
        """
        try:
            headers = {'Content-type': 'application/json'}
            request_body = {"results": self.get_all_files_for_report(allure_results_directory=allure_results_directory)}
            json_request_body = json.dumps(request_body)
            ssl_verification = True

            self.logger.debug("------------------SEND-ALLURE-RESULTS------------------")
            url = (f"{allure_server}/allure-docker-service/send-results?project_id={project_id}&force_project_creation="
                   f"{'true' if create_project else 'false'}")
            response = requests.post(url, headers=headers, data=json_request_body, verify=ssl_verification, timeout=300)
            self.logger.debug(f"STATUS CODE: {response.status_code}")
            if response.status_code != 200:
                self.logger.debug("RESPONSE:")
                json_response_body = json.loads(response.content)
                json_prettier_response_body = json.dumps(json_response_body, indent=4, sort_keys=True)
                self.logger.debug(json_prettier_response_body)
        except Exception as err:
            self.logger.error(f"Failed to send results: {err}")
            raise ValueError(err)

    def clean_results(self, allure_server=None, project_id=None):
        """

        :return:
        """
        try:
            allure_server = allure_server or self.allure_server
            project_id = project_id or 'default'
            headers = {'Content-type': 'application/json'}
            ssl_verification = True

            self.logger.debug("------------------CLEAN-RESULTS------------------")
            url = f"{allure_server}/allure-docker-service/clean-results?project_id={project_id}"
            response = requests.get(url, headers=headers, verify=ssl_verification, timeout=60)

            self.logger.debug(f"STATUS CODE: {response.status_code}")
            if response.status_code != 200:
                self.logger.debug("RESPONSE:")
                json_response_body = json.loads(response.content)
                json_prettier_response_body = json.dumps(json_response_body, indent=4, sort_keys=True)
                self.logger.debug(json_prettier_response_body)
            return response
        except Exception as err:
            self.logger.error(f"Failed to clean reporting results: {err}")
            raise ValueError(err)

    def clean_history(self, allure_server=None, project_id=None):
        """

        :return:
        """
        try:
            allure_server = allure_server or self.allure_server
            project_id = project_id or 'default'
            headers = {'Content-type': 'application/json'}
            ssl_verification = True

            url = f"{allure_server}/allure-docker-service/clean-history?project_id={project_id}"

            self.logger.debug("------------------CLEAN-HISTORY------------------")
            response = requests.get(url, headers=headers, verify=ssl_verification, timeout=60)

            self.logger.debug(f"STATUS CODE: {response.status_code}")
            if response.status_code != 200:
                self.logger.debug("RESPONSE:")
                json_response_body = json.loads(response.content)
                json_prettier_response_body = json.dumps(json_response_body, indent=4, sort_keys=True)
                self.logger.debug(json_prettier_response_body)
            return response
        except Exception as err:
            self.logger.error(f"Failed to clean reporting history: {err}")
            raise ValueError(err)

    def get_project_reports(self, allure_server=None, project_id=None):
        """

        :param allure_server:
        :param project_id:
        :param silent:
        :return:
        """
        try:
            self.logger.debug(f"Getting allure project {project_id}")
            allure_server = allure_server or self.allure_server
            url = f"{allure_server}/allure-docker-service/projects/{project_id}"
            headers = {'Content-type': 'application/json'}
            response = requests.get(url, headers=headers, timeout=180)
            self.logger.debug(f"STATUS CODE: {response.status_code}")
            json_response_body = json.loads(response.content)
            reports = json_response_body["data"]["project"]["reports"]
            return reports
        except Exception as err:
            self.logger.error(f"Failed to get project reports: {err}")
            raise ValueError(err)

    @retry.retry(ValueError, tries=20, delay=10)
    def generate_latest_report_link(self, allure_server=None, project_id=None):
        """

        :param allure_server:
        :param project_id:
        :return:
        """
        try:
            allure_server = allure_server or self.allure_server
            self.logger.debug(f"Generating allure report link for project id {project_id}")
            link = f'{allure_server}/allure-docker-service/projects/{project_id}/reports/latest/index.html'
            project_reports_links = self.get_project_reports(allure_server=allure_server, project_id=project_id)

            if link not in project_reports_links:
                raise ValueError(f"Failed to retrieve latest report link,for project {project_id}. retrying")

            self.logger.debug(f"allure results link is: {link}")
            return link
        except Exception as err:
            self.logger.debug(f"Failed generating allure report link for project id {project_id}. retrying")
            raise ValueError(f"Failed generating allure report link for project id {project_id}: {err}")

    def delete_allure_results_dir_content(self, allure_results_directory=None):
        """

        :return:
        """
        try:
            dir_path = allure_results_directory
            self.logger.debug(f"Deleting allure results directory: {dir_path} contents")
            if _files.check_if_directory_exist(dir_path):
                _files.delete_directory_contents(dir_path)
        except Exception as err:
            self.logger.warning(f"Failed to delete allure results directory {dir_path} contents: {err}")

    def delete_allure_results_dir(self, allure_results_directory=None):
        """

        :return:
        """
        try:
            dir_path = allure_results_directory or self.allure_dir
            self.logger.debug(f"Deleting allure results directory: {dir_path}")
            if _files.check_if_directory_exist(dir_path):
                shutil.rmtree(dir_path)
        except Exception as err:
            self.logger.warning(f"Failed to delete allure results directory {dir_path}: {err}")
