import os
import sys

import pytest

from framework.infra.infra import Infra
from tfls.tfl import TFL
from tests.sanity.data import Data

sys.path.append(os.getcwd())


class TestSuiteSanity:
    """
    A suite to test sanity use cases for all rest APIs
    data contains all suites predefined data, and can be edited at any time during run time
    """
    data: Data = Data

    # @pytest.mark.parametrize('my_value', Data.my_variables)
    def test_create_integration(self, infra: Infra, TFL: TFL, setup, teardown):
        """
        A test for validating basic create integration rest API
        :param infra: a fixture for exposing all infra/framework functionality
        :param TFL: a fixture to expose all tests steps embedded in the TFL layer
        :param setup: a fixture for executing setup operation as preparation for the test
        :param teardown: a fixture for executing teardown/cleanup operation after the test
        :return: None
        """
        TFL.integrations.step_create_integration(tenant=self.data.tenant1, name='integration_0', type='type_0')
        TFL.integrations.step_validate_integration_found(tenant=self.data.tenant1, name='integration_0', type='type_0')


    def test_delete_integration(self, infra: Infra, TFL: TFL, setup, teardown):
        """
        A test for validating basic delete integration rest API
        :param infra: a fixture for exposing all infra/framework functionality
        :param TFL: a fixture to expose all tests steps embedded in the TFL layer
        :param setup: a fixture for executing setup operation as preparation for the test
        :param teardown: a fixture for executing teardown/cleanup operation after the test
        :return: None
        """
        TFL.integrations.step_create_integration(tenant=self.data.tenant1, name='integration_0', type='type_0')
        TFL.integrations.step_validate_integration_found(tenant=self.data.tenant1, name='integration_0',
                                                         type='type_0')
        TFL.integrations.step_delete_integration(tenant=self.data.tenant1, name='integration_0', type='type_0')
        TFL.integrations.step_validate_integration_found(tenant=self.data.tenant1, name='integration_0',
                                                         type='type_0', positive=False)


    def test_update_integration(self, infra: Infra, TFL: TFL, setup, teardown):
        """
        A test for validating basic update integration rest API
        :param infra: a fixture for exposing all infra/framework functionality
        :param TFL: a fixture to expose all tests steps embedded in the TFL layer
        :param setup: a fixture for executing setup operation as preparation for the test
        :param teardown: a fixture for executing teardown/cleanup operation after the test
        :return: None
        """
        TFL.integrations.step_create_integration(tenant=self.data.tenant1, name='integration_0', type='type_0')
        TFL.integrations.step_validate_integration_found(tenant=self.data.tenant1, name='integration_0',
                                                         type='type_0')
        TFL.integrations.step_update_integration(tenant=self.data.tenant1, name='integration_0', type='type_0',
                                                 new_name="integration_0_updated")
        TFL.integrations.step_validate_integration_found(tenant=self.data.tenant1, name='integration_0_updated',
                                                         type='type_0', positive=True)

    def test_get_integration_by_id(self, infra: Infra, TFL: TFL, setup, teardown):
        """
        A test for validating basic get integration by id rest API
        :param infra: a fixture for exposing all infra/framework functionality
        :param TFL: a fixture to expose all tests steps embedded in the TFL layer
        :param setup: a fixture for executing setup operation as preparation for the test
        :param teardown: a fixture for executing teardown/cleanup operation after the test
        :return: None
        """
        integration = TFL.integrations.step_create_integration(tenant=self.data.tenant1, name='integration_0',
                                                                      type='type_0').json()
        TFL.integrations.step_validate_integration_found(tenant=self.data.tenant1, name='integration_0', type='type_0')
        TFL.integrations.step_get_integration_by_id(tenant=self.data.tenant1, integration_id = integration['id'])


    def test_get_all_integrations(self, infra: Infra, TFL: TFL, setup, teardown):
        """
        A test for validating basic get all integrations rest API
        :param infra: a fixture for exposing all infra/framework functionality
        :param TFL: a fixture to expose all tests steps embedded in the TFL layer
        :param setup: a fixture for executing setup operation as preparation for the test
        :param teardown: a fixture for executing teardown/cleanup operation after the test
        :return: None
        """
        TFL.integrations.step_create_integrations(tenant=self.data.tenant1, integrations=self.data.integrations)
        TFL.integrations.step_validate_integrations_found(tenant=self.data.tenant1, integrations=self.data.integrations)


    def test_create_asset(self, infra: Infra, TFL: TFL, setup, teardown):
        """
        A test for validating basic create asset rest API
        :param infra: a fixture for exposing all infra/framework functionality
        :param TFL: a fixture to expose all tests steps embedded in the TFL layer
        :param setup: a fixture for executing setup operation as preparation for the test
        :param teardown: a fixture for executing teardown/cleanup operation after the test
        :return: None
        """
        integration = TFL.integrations.step_create_integration(tenant=self.data.tenant1, name='integration_0',
                                                               type='type_0').json()
        TFL.assets.step_create_asset(tenant=self.data.tenant1, integration_id=integration['id'],
                                     name="asset_0", description="asset_0_description")
        TFL.assets.step_validate_asset_found(tenant=self.data.tenant1, integration_id=integration['id'],
                                             name='asset_0', description='asset_0_description')


    def test_delete_asset(self, infra: Infra, TFL: TFL, setup, teardown):
        """
        A test for validating basic delete asset rest API
        :param infra: a fixture for exposing all infra/framework functionality
        :param TFL: a fixture to expose all tests steps embedded in the TFL layer
        :param setup: a fixture for executing setup operation as preparation for the test
        :param teardown: a fixture for executing teardown/cleanup operation after the test
        :return: None
        """
        integration = TFL.integrations.step_create_integration(tenant=self.data.tenant1, name='integration_0',
                                                               type='type_0').json()
        asset = TFL.assets.step_create_asset(tenant=self.data.tenant1, integration_id=integration['id'],
                                             name="asset_0", description="asset_0_description").json()
        TFL.assets.step_validate_asset_found_by_id(tenant=self.data.tenant1, asset_id=asset['id'],
                                                   name='asset_0', description='asset_0_description')
        TFL.assets.step_delete_asset(tenant=self.data.tenant1, asset_id=asset['id'])
        TFL.assets.step_validate_asset_found_by_id(tenant=self.data.tenant1, asset_id=asset['id'],
                                                   name='asset_0', description='asset_0_description', positive=False)


    def test_update_asset(self, infra: Infra, TFL: TFL, setup, teardown):
        """
        A test for validating basic update asset rest API
        :param infra: a fixture for exposing all infra/framework functionality
        :param TFL: a fixture to expose all tests steps embedded in the TFL layer
        :param setup: a fixture for executing setup operation as preparation for the test
        :param teardown: a fixture for executing teardown/cleanup operation after the test
        :return: None
        """
        integration = TFL.integrations.step_create_integration(tenant=self.data.tenant1, name='integration_0',
                                                               type='type_0').json()
        asset = TFL.assets.step_create_asset(tenant=self.data.tenant1, integration_id=integration['id'],
                                             name="asset_0", description="asset_0_description").json()
        TFL.assets.step_validate_asset_found_by_id(tenant=self.data.tenant1, asset_id=asset['id'],
                                                   name='asset_0', description='asset_0_description')
        TFL.assets.step_update_asset(tenant=self.data.tenant1, asset_id=asset['id'], new_name="asset_0_updated",
                                     new_description="asset_0_description_updated")
        TFL.assets.step_validate_asset_found_by_id(tenant=self.data.tenant1, asset_id=asset['id'],
                                                   name='asset_0_updated', description='asset_0_description_updated')


    def test_list_assets_by_integration_id(self, infra: Infra, TFL: TFL, setup, teardown):
        """
        A test for validating basic list assets by integration id rest API
        :param infra: a fixture for exposing all infra/framework functionality
        :param TFL: a fixture to expose all tests steps embedded in the TFL layer
        :param setup: a fixture for executing setup operation as preparation for the test
        :param teardown: a fixture for executing teardown/cleanup operation after the test
        :return: None
        """
        integration = TFL.integrations.step_create_integration(tenant=self.data.tenant1, name='integration_0',
                                                               type='type_0').json()
        assets_ids = TFL.assets.step_create_assets(tenant=self.data.tenant1, integration_id=integration['id'],
                                                   assets=self.data.assets)

        TFL.assets.step_validate_assets_found_by_id(tenant=self.data.tenant1, assets_ids=assets_ids)


    def test_get_asset_by_id(self, infra: Infra, TFL: TFL, setup, teardown):
        """
        A test for validating basic get asset by id rest API
        :param infra: a fixture for exposing all infra/framework functionality
        :param TFL: a fixture to expose all tests steps embedded in the TFL layer
        :param setup: a fixture for executing setup operation as preparation for the test
        :param teardown: a fixture for executing teardown/cleanup operation after the test
        :return: None
        """
        integration = TFL.integrations.step_create_integration(tenant=self.data.tenant1, name='integration_0',
                                                               type='type_0').json()
        asset = TFL.assets.step_create_asset(tenant=self.data.tenant1, integration_id=integration['id'],
                                             name="asset_0", description="asset_0_description").json()
        TFL.assets.step_validate_asset_found_by_id(tenant=self.data.tenant1, asset_id=asset['id'],
                                                   name='asset_0', description='asset_0_description')




# ############################################## FIXTURES #####################################################


    @pytest.fixture()
    def setup(self, infra: Infra, TFL: TFL):
        """
        a fixture for executing setup operation as preparation for a test
        :param infra: a fixture for exposing all infra/framework functionality
        :param TFL: a fixture to expose all tests steps embedded in the TFL layer
        :return: None
        """
        yield

    @pytest.fixture()
    def teardown(self, infra: Infra, TFL: TFL):
        """
        a fixture for executing teardown/cleanup operation after a test
        :param infra: a fixture for exposing all infra/framework functionality
        :param TFL: a fixture to expose all tests steps embedded in the TFL layer
        :return: None
        """
        yield
        TFL.integrations.step_delete_all_integrations(tenant=self.data.tenant1)
        TFL.integrations.step_delete_all_integrations(tenant=self.data.tenant2)



    @pytest.fixture(autouse=True, scope='function')
    def initialize_data(self, infra: Infra, TFL: TFL):
        """
        a fixture for initializing the suite data object
        :param infra: a fixture for exposing all infra/framework functionality
        :param TFL: a fixture to expose all tests steps embedded in the TFL layer
        :return: None
        """
        self.data = Data(infra=infra)
        yield