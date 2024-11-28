from framework.tfls.base_tfl import BaseTfl


class AssetsOps(BaseTfl):
    def __init__(self, infra=None, logger=None, tfls=None):
        super().__init__(infra=infra, logger=logger, tfls=tfls)

    @BaseTfl.step_wrapper(title="step_list_all_assets", error="Failed to list all assets")
    def step_list_all_assets(self, tenant, integration_id, positive=True, **kwargs):
        """

        :param tenant:
        :param integration_id:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"listing all assets for tenant {tenant.tid} and integration {integration_id}")
        response = self.infra.rest.assets.list_assets_by_integration_id(tenant=tenant, integration_id=integration_id)
        if positive:
            if response.status_code != 200:
                raise ValueError(
                    f"Failed to list all assets: status_code: {response.status_code} content: {response.content}")
        else:
            if response.status_code == 200:
                raise ValueError(
                    f"Unexpectedly succeeded to list all assets: status_code: {response.status_code} "
                    f"content: {response.content}")


    @BaseTfl.step_wrapper(title="step_create_asset", error="Failed to create asset")
    def step_create_asset(self, tenant, integration_id, name, description="", positive=True, **kwargs):
        """

        :param tenant:
        :param integration_id:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"creating asset {name} for tenant {tenant.tid} and integration {integration_id}")
        response = self.infra.rest.assets.create_asset(tenant=tenant, integration_id=integration_id,
                                                       description=description, name=name)
        if positive:
            if response.status_code != 201:
                raise ValueError(
                    f"Failed to create asset {name} for integration {integration_id} and tenant "
                    f"{tenant.tid}: status_code: {response.status_code} content: {response.content}")
        else:
            if response.status_code == 201:
                raise ValueError(
                    f"Unexpectedly succeeded to create asset {name} for integration {integration_id} and tenant "
                    f"{tenant.tid}: status_code: {response.status_code} content: {response.content}")
        return response

    @BaseTfl.step_wrapper(title="step_create_asset", error="Failed to create asset")
    def step_create_assets(self, tenant, integration_id, assets, positive=True, **kwargs):
        """

        :param tenant:
        :param integration_id:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"creating assets for tenant {tenant.tid} and integration {integration_id}")
        assets_ids = []
        for asset in assets:
            self.logger.debug(f"creating asset {asset['name']} under tenant {tenant.tid} and "
                              f"integration {integration_id}")
            response = self.infra.rest.assets.create_asset(tenant=tenant, integration_id=integration_id,
                                                           description=asset['description'], name=asset['name'])
            if positive:
                if response.status_code != 201:
                    raise ValueError(
                        f"Failed to create asset {asset['name']} for integration {integration_id} and tenant "
                        f"{tenant.tid}: status_code: {response.status_code} content: {response.content}")
                else:
                    assets_ids.append(response.json()['id'])
            else:
                if response.status_code == 201:
                    raise ValueError(
                        f"Unexpectedly succeeded to create asset {asset['name']} for integration {integration_id} "
                        f"and tenant {tenant.tid}: status_code: {response.status_code} content: {response.content}")
        return assets_ids


    @BaseTfl.step_wrapper(title="step_validate_asset_found", error="Failed to validate asset found")
    def step_validate_asset_found(self, tenant, integration_id, name, description="", positive=True, **kwargs):
        """

        :param tenant:
        :param integration_id:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"Validating asset {name} with description {description} "
                         f"{'exist' if positive else 'does not exist'} for tenant {tenant.tid} and "
                         f"integration {integration_id}")
        response = self.infra.rest.assets.list_assets_by_integration_id(tenant=tenant, integration_id=integration_id)
        assets_found = [asset for asset in response.json()] if response.json() else []
        found = False
        for asset in assets_found:
            if asset['name'] == name and asset['description'] == description:
                found = True
                break

        if positive and not found:
            raise ValueError(f"Asset {name} with description {description} was not found under integration "
                             f"{integration_id} and tenant {tenant.tid}")
        if not positive and found:
                raise ValueError(f"Unexpectedly found asset {name} with description {description} under integration "
                                 f"{integration_id} and tenant {tenant.tid}")


    @BaseTfl.step_wrapper(title="step_validate_asset_found", error="Failed to validate asset found")
    def step_validate_asset_found_by_id(self, tenant, asset_id, name=None, description=None, positive=True, **kwargs):
        """

        :param tenant:
        :param integration_id:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"Validating asset {asset_id} {'exist' if positive else 'does not exist'} for tenant "
                         f"{tenant.tid}")
        response = self.infra.rest.assets.get_asset_by_id(tenant=tenant, asset_id=asset_id)

        if positive and response.status_code != 200:
            raise ValueError(f"Asset {asset_id} was not found under tenant {tenant.tid}")
        if not positive and response.status_code == 200:
            raise ValueError(f"Unexpectedly found asset {asset_id} with description {description} under "
                             f"tenant {tenant.tid}")
        if name and positive and response.json()['name'] != name:
            raise ValueError(f"Asset {asset_id} was found under tenant {tenant.tid} but with unexpected name "
                             f"{response['name']}")
        if description and positive and response.json()['description'] != description:
            raise ValueError(f"Asset {asset_id} was found under tenant {tenant.tid} but with unexpected description "
                             f"{response['description']}")

    @BaseTfl.step_wrapper(title="step_validate_asset_found", error="Failed to validate asset found")
    def step_validate_assets_found_by_id(self, tenant, assets_ids, positive=True, **kwargs):
        """

        :param tenant:
        :param integration_id:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"Validating assets {'exist' if positive else 'does not exist'} for tenant "
                         f"{tenant.tid}")
        for asset_id in assets_ids:
            response = self.infra.rest.assets.get_asset_by_id(tenant=tenant, asset_id=asset_id)

            if positive and response.status_code != 200:
                raise ValueError(f"Asset {asset_id} was not found under tenant {tenant.tid}")
            if not positive and response.status_code == 200:
                raise ValueError(f"Unexpectedly found asset {asset_id} under tenant {tenant.tid}")


    @BaseTfl.step_wrapper(title="step_delete_asset", error="Failed to delete asset")
    def step_delete_asset(self, tenant, asset_id, positive=True, **kwargs):
        """

        :param tenant:
        :param integration_id:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"deleting asset {asset_id} from tenant {tenant.tid}")
        response = self.infra.rest.assets.delete_asset(tenant=tenant, asset_id=asset_id)

        if positive and response.status_code != 204:
            raise ValueError(f"Failed to delete asset {asset_id} from tenant {tenant.tid}")
        if not positive and response.status_code == 204:
                raise ValueError(f"Unexpectedly succeeded to delete asset {asset_id} from tenant {tenant.tid}")


    @BaseTfl.step_wrapper(title="step_update_asset", error="Failed to update asset")
    def step_update_asset(self, tenant, asset_id, new_name, new_description, positive=True, **kwargs):
        """

        :param tenant:
        :param integration_id:
        :param positive:
        :param kwargs:
        :return:
        """
        self.logger.info(f"updating asset {asset_id} from tenant {tenant.tid} with new name {new_name} and new "
                         f"description {new_description}")
        response = self.infra.rest.assets.update_asset(tenant=tenant, asset_id=asset_id, asset_name=new_name,
                                                       asset_description=new_description)

        if positive and response.status_code != 200:
            raise ValueError(f"Failed to update asset {asset_id} from tenant {tenant.tid}")
        if not positive and response.status_code == 20:
                raise ValueError(f"Unexpectedly succeeded to update asset {asset_id} from tenant {tenant.tid}")