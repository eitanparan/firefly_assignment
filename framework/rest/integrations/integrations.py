from requests.auth import HTTPBasicAuth

from framework.rest.base_rest import BaseRest
from framework.rest.integrations.rdo import RdoIntegrations


class Integrations(BaseRest):
    """
    Class for representing REST client for integrations calls
    """

    def __init__(self):
        super().__init__()
        self.rdo = RdoIntegrations(base_url="http://localhost:8080/api/v1/integrations",
                                   headers={"accept": "application/json", "Content-Type": "application/json"})

    def list_integrations(self, tenant):
        """

        :return:
        """
        try:
            self.logger.info(f"Getting integrations of tenant {tenant.tid}")
            auth = HTTPBasicAuth(tenant.user, tenant.password)
            resp = self.get(url=self.rdo.list_integrations.url, headers=self.rdo.list_integrations.headers, auth=auth)
            return resp
        except Exception as err:
            raise Exception(f"Failed to get integrations: {err}")


    def update_integration(self, tenant, integration_id: str, name: str):
        """

        :return:
        """
        try:
            self.logger.info(f"Updating tenant {tenant.tid} integration {integration_id} with new name {name}")
            payload = {"id": integration_id, "name": name}
            auth = HTTPBasicAuth(tenant.user, tenant.password)
            resp = self.put(url=self.rdo.update_integration.url, payload=payload,
                            headers=self.rdo.update_integration.headers, auth=auth)
            return resp
        except Exception as err:
            raise Exception(f"Failed to update integration {integration_id} with new name {name}: {err}")


    def create_integration(self, tenant, name: str, type: str):
        """

        :return:
        """
        try:
            self.logger.info(f"Creating new integration of type {type} and name {name} for tenant {tenant.tid}")
            payload = {"type": type, "name": name}
            auth = HTTPBasicAuth(tenant.user, tenant.password)
            resp = self.post(url=self.rdo.create_integration.url, payload=payload,
                             headers=self.rdo.create_integration.headers, auth=auth)
            return resp
        except Exception as err:
            raise Exception(f"Failed to create new integration of type {type} and name {name}: {err}")


    def get_integration_by_id(self, tenant, integration_id):
        """

        :return:
        """
        try:
            self.logger.info(f"Getting integration {integration_id} for tenant {tenant.tid}")
            auth = HTTPBasicAuth(tenant.user, tenant.password)
            resp = self.get(url=self.rdo.get_integration_by_id.url.format(integration_id=integration_id),
                            headers=self.rdo.get_integration_by_id.headers, auth=auth)
            return resp
        except Exception as err:
            raise Exception(f"Failed to get integrations: {err}")


    def delete_integration(self, tenant, integration_id):
        """

        :return:
        """
        try:
            self.logger.info(f"Deleting integration with id {integration_id} from tenant {tenant.tid}")
            auth = HTTPBasicAuth(tenant.user, tenant.password)
            resp = self.delete(url=self.rdo.delete_integration.url.format(integration_id=integration_id),
                               headers=self.rdo.delete_integration.headers, auth=auth)
            return resp
        except Exception as err:
            raise Exception(f"Failed to delete integration with id {integration_id}: {err}")

    def get_integration_by_name_and_type(self, tenant, name, type):
        """

        :param tenant:
        :param name:
        :param type:
        :return:
        """
        try:
            self.logger.info(f"Fetching integration with name {name} and type {type} from tenant {tenant.tid}")
            integrations = self.list_integrations(tenant=tenant).json()
            if integrations:
                for item in integrations:
                    if item['name'] == name and item['type'] == type:
                        return item
        except Exception as err:
            raise Exception(f"Failed to fetch integration with name {name} and type {type} "
                            f"from tenant {tenant.tid}: {err}")
