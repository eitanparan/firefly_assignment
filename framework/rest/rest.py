from framework.rest.base_rest import BaseRest
from framework.logger.logger import Logger
from framework.rest.assets.assets import Assets
from framework.rest.integrations.integrations import Integrations


class Rest(BaseRest):
    """
    A class for grouping all rest-based instances
    """

    def __init__(self):
        super().__init__()
        self.logger = Logger('Rest').logger
        self.assets: Assets = Assets()
        self.integrations: Integrations = Integrations()
