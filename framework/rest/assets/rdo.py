from framework.rest.base_rest import RdoObject


class RdoAssets:
    """
    Rest Data Objects for assets
    """

    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers
        self.list_assets_by_integration_id = RdoObject(url=f"{self.base_url}" + '/{integration_id}{page}{limit}',
                                                       headers=self.headers)
        self.create_asset = RdoObject(url=f"{self.base_url}", headers=self.headers)
        self.update_asset = RdoObject(url=f"{self.base_url}", headers=self.headers)
        self.get_asset_by_id = RdoObject(url=f"{self.base_url}" + '/{asset_id}', headers=self.headers)
        self.delete_asset = RdoObject(url=f"{self.base_url}" + '/{asset_id}', headers=self.headers)

