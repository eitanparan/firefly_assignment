import os
import sys

import pytest

from framework.infra.infra import Infra
from tfls.tfl import TFL
from tests.stress.data import Data

sys.path.append(os.getcwd())


class TestSuiteStress:
    """
    A suite to test stress and load on the service
    data contains all suites predefined data, and can be edited at any time during run time
    """
    data: Data = Data

    # @pytest.mark.parametrize('my_value', Data.my_variables)
    def test_stress_get_integrations(self, infra: Infra, TFL: TFL, setup, teardown):
        """
        A test for validating stress use case where we test a number of parallel calls within one minute
        :param infra: a fixture for exposing all infra/framework functionality
        :param TFL: a fixture to expose all tests steps embedded in the TFL layer
        :param setup: a fixture for executing setup operation as preparation for the test
        :param teardown: a fixture for executing teardown/cleanup operation after the test
        :return: None
        """
        TFL.integrations.step_create_integrations(tenant=self.data.tenant1, integrations=self.data.integrations)
        TFL.integrations.step_stress_list_all_integrations(tenant=self.data.tenant1, num_of_calls_per_minute=1000)




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
        a fixture for executing teardown/cleanup operation after a test.
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