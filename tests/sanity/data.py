from framework.infra.infra import Infra

class Data:
    my_variables = ['1']

    def __init__(self, infra: Infra = None):
        __test__ = False
        self.infra = infra

        self.tenant1 = Tenant(tid='tenant1', user='test1', password='test123')
        self.tenant2 = Tenant(tid='tenant2', user='test2', password='test456')


        self.integrations = [{'name': 'test_integration_0', 'type': 'test_integration_type_0'},
                             {'name': 'test_integration_1', 'type': 'test_integration_type_1'},
                             {'name': 'test_integration_2', 'type': 'test_integration_type_2'},
                             {'name': 'test_integration_3', 'type': 'test_integration_type_3'},
                             {'name': 'test_integration_4', 'type': 'test_integration_type_4'},
                             {'name': 'test_integration_5', 'type': 'test_integration_type_5'},
                             {'name': 'test_integration_6', 'type': 'test_integration_type_6'},
                             {'name': 'test_integration_7', 'type': 'test_integration_type_7'},
                             {'name': 'test_integration_8', 'type': 'test_integration_type_8'},
                             {'name': 'test_integration_9', 'type': 'test_integration_type_9'}]

        self.assets = [{'name': 'test_asset_0', 'description': 'test_asset_description_0'},
                       {'name': 'test_asset_1', 'description': 'test_asset_description_1'},
                       {'name': 'test_asset_2', 'description': 'test_asset_description_2'},
                       {'name': 'test_asset_3', 'description': 'test_asset_description_3'},
                       {'name': 'test_asset_4', 'description': 'test_asset_description_4'},
                       {'name': 'test_asset_5', 'description': 'test_asset_description_5'},
                       {'name': 'test_asset_6', 'description': 'test_asset_description_6'},
                       {'name': 'test_asset_7', 'description': 'test_asset_description_7'},
                       {'name': 'test_asset_8', 'description': 'test_asset_description_8'},
                       {'name': 'test_asset_9', 'description': 'test_asset_description_9'}]


class Tenant:
    def __init__(self, tid, user, password):
        self.tid = tid
        self.user = user
        self.password = password
