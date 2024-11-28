from framework.rest.base_rest import RdoObject


class RdoIntegrations:
    """
    Rest Data Objects for integrations
    """

    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers
        self.list_integrations = RdoObject(url=f"{self.base_url}", headers=self.headers)
        self.update_integration = RdoObject(url=f"{self.base_url}", headers=self.headers)
        self.create_integration = RdoObject(url=f"{self.base_url}", headers=self.headers)
        self.get_integration_by_id = RdoObject(url=f"{self.base_url}" + '/{integration_id}', headers=self.headers)
        self.delete_integration = RdoObject(url=f"{self.base_url}" + '/{integration_id}', headers=self.headers)
