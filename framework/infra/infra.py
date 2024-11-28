from framework.rest.rest import Rest
from framework.logger.logger import Logger
from framework.general.general import General


class Infra:
    """
    A class for exposing the framework layer rest modules
    """
    def __init__(self):
        """

        """
        self.logger = Logger('Infra').logger
        self.logger.warning(f"Starting initialization of infra instance")
        self.general = General()
        self.rest: Rest = Rest()
        self.logger.warning(f"infra initialization finished successfully for instance")
