from requests.auth import HTTPBasicAuth

from framework.rest.base_rest import BaseRest
from framework.rest.assets.rdo import RdoAssets


class Assets(BaseRest):
    """
    Class for representing REST client for assets calls
    """

    def __init__(self):
        super().__init__()
        self.rdo = RdoAssets(base_url="http://localhost:8080/api/v1/assets",
                             headers={"accept": "application/json", "Content-Type": "application/json"})

    def list_assets_by_integration_id(self, tenant, integration_id, page=None, limit=None):
        """

        :return:
        """
        try:
            self.logger.info(f"Getting assets of tenant {tenant.tid} and integration {integration_id}")
            page = f"?page={page}" if page else ''
            limit = f"?limit={limit}" if limit else ''
            integration_id = f"?integrationId={integration_id}"
            auth = HTTPBasicAuth(tenant.user, tenant.password)
            resp = self.get(url=self.rdo.list_assets_by_integration_id.url.format(integration_id=integration_id,
                                                                                  page=page, limit=limit),
                            headers=self.rdo.list_assets_by_integration_id.headers, auth=auth)
            return resp
        except Exception as err:
            raise Exception(f"Failed to create new asset for integration id {integration_id}: {err}")


    def create_asset(self, tenant, integration_id: str, description: str="", name: str=""):
        """

        :return:
        """
        try:
            self.logger.info(f"Creating new asset for integration id {integration_id} and tenant {tenant.tid}")
            payload = {"integrationId": integration_id, "description": description, "name": name}
            auth = HTTPBasicAuth(tenant.user, tenant.password)
            resp = self.post(url=self.rdo.create_asset.url, payload=payload, headers=self.rdo.create_asset.headers,
                             auth=auth)
            return resp
        except Exception as err:
            raise Exception(f"Failed to create watch: {err}")


    def update_asset(self, tenant, asset_id: str, asset_description: str="", asset_name: str=""):
        """

        :return:
        """
        try:
            self.logger.info(f"Updating asset {asset_id} with name {asset_name} and description {asset_description}"
                             f"for tenant {tenant.tid}")
            payload = {"id": asset_id, "description": asset_description, "name": asset_name}
            auth = HTTPBasicAuth(tenant.user, tenant.password)
            resp = self.patch(url=self.rdo.update_asset.url, payload=payload, headers=self.rdo.update_asset.headers,
                              auth=auth)
            return resp
        except Exception as err:
            raise Exception(f"Failed to update asset {asset_id} with name {asset_name} and description "
                            f"{asset_description}: {err}")


    def get_asset_by_id(self, tenant, asset_id):
        """

        :return:
        """
        try:
            self.logger.info(f"Getting asset {asset_id} from tenant {tenant.tid}")
            auth = HTTPBasicAuth(tenant.user, tenant.password)
            resp = self.get(url=self.rdo.get_asset_by_id.url.format(asset_id=asset_id),
                            headers=self.rdo.get_asset_by_id.headers, auth=auth)
            return resp
        except Exception as err:
            raise Exception(f"Failed to get asset with id {asset_id}: {err}")


    def delete_asset(self, tenant, asset_id):
        """

        :return:
        """
        try:
            self.logger.info(f"Deleting asset with id {asset_id} from tenant {tenant.tid}")
            auth = HTTPBasicAuth(tenant.user, tenant.password)
            resp = self.delete(url=self.rdo.delete_asset.url.format(asset_id=asset_id),
                               headers=self.rdo.delete_asset.headers, auth=auth)
            return resp
        except Exception as err:
            raise Exception(f"Failed to delete asset with id {asset_id}: {err}")