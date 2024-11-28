from framework.infra.infra import Infra
from tfls.integrations.integration_ops import IntegrationsOps
from tfls.assets.assets_ops import AssetsOps


class TFL:
    """
    This object initializes all TFLs
    Each TFL attribute will hold all of the tests steps grouped under its domain
    It also share self between its attributes so each TFL can call other TFLs
    """

    def __init__(self, infra: Infra):
        self.integrations: IntegrationsOps = IntegrationsOps(infra=infra, tfls=self)
        self.assets: AssetsOps = AssetsOps(infra=infra, tfls=self)
