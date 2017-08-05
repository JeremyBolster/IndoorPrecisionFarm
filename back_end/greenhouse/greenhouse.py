from back_end.configuration import Config
from back_end.databases.time_series_database_connection import TSDataBaseConnector
from back_end.greenhouse.communication.communication import Communication
from back_end.greenhouse.environment.environment import Environment
from back_end.greenhouse.environment.environmental_control import EnvironmentalControl
from back_end.greenhouse.communication.simulated_arduino import ArduinoSimulated

import logging
import yaml
import os


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
        self.greenhouse = None
        self.current_state = None
        self.remote_store = None
        self.pattern = None
        self.control = None

    def setup(self, greenhouse: Communication, climate_pattern: str, remote_store: TSDataBaseConnector=None) -> None:
        self.greenhouse = greenhouse
        self.current_state = Environment()
        self.remote_store = remote_store
        climate_file_name = os.path.join(
            os.path.dirname(__file__),
            os.path.pardir,
            'default_climate.yaml')
        if climate_pattern:
            climate_file_name = os.path.abspath(climate_pattern)
        with open(climate_file_name) as f:
            self.pattern = yaml.safe_load(f.read())
        # TODO set the current state of the greenhouse to the desired state at the beginning
        self.control = EnvironmentalControl(self.greenhouse, self.current_state)

    def run(self):
        """
        This function runs the current pattern in the greenhouse. It runs this in a daemonized thread.
        :return:
        """
        pass
