from back_end.configuration import Config
from back_end.greenhouse.communication.communication import Communication

import logging


class Greenhouse(object):
    """
    The greenhouse class is a complete system for controlling a greenhouse. It contains all of the following:
    1. Communication to the greenhouse
    2. Environmental Control of the Greenhouse
    3. The current state of the Greenhouse
    4. A pattern to match climate with
    5. A reference to a networked data store to push state to
    It is responsible for fetching the current state of the greenhouse and pushing that status to a networked data store
    and to a local reference of current state for use by the environmental control system
    """
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.config = Config.config

    def setup(self,
              greenhouse: Communication,
              climate_pattern: str='./default_climate.yaml',
              remote_store=None) -> None:
        # TODO add a type to remote store so that I can figure out how to use it
        pass
