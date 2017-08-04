from back_end.configuration import Config
from back_end.communication.communication import Communication
from back_end.environment.environment import Environment

import threading
from threading import Thread

import logging
import time

REFRESH_INTERVAL = 10


class EnvironmentalControl(object):
    def __init__(self, greenhouse: Communication):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.config = Config.config
        self.greenhouse = greenhouse
        self.environment = None
        self.lock = threading.Lock()
        self.set_up_thread()

    def set_up_thread(self):
        th = Thread(target=self._set_environment)
        th.daemon = True
        th.start()

    def set_environment(self, desired_environment: Environment) -> None:
        """
        This is the main function of this class. This function takes a given environment and applies it to its assigned
        communication device / greenhouse.
        :param desired_environment: A desired environment to create
        :return: None
        """
        with self.lock:
            self.environment = desired_environment

    def _set_environment(self) -> None:
        """
        This function updates the environment to whatever value is
        :return: None
        """
        while True:
            time.sleep(REFRESH_INTERVAL)
            with self.lock:
                if self.environment:
                    # By passing environment as a reference we can let this call be threaded
                    th = Thread(target=self._update_environment, args=[self.environment])
                    th.daemon = True
                    th.start()

    def _update_environment(self, environment: Environment) -> None:
        """
        This is a function that takes the current desired environment and applies it to this objects assigned
        greenhouse.
        :param environment: The desired environment
        :return: None
        """
        self._water_temp(environment.water_temp)  # only works if hydroponic
        self._ph(environment.ph)  # Handles either soil or water ph
        self._soil_moisture(environment.soil_moisture)  # only works if soil based
        self._air_temp(environment.air_temp)
        self._circulation(environment.circulation)
        self._co2(environment.co2)
        self._lighting(environment.light_level)
        self._humidity(environment.humidity)

    def _water_temp(self, desired):
        pass

    def _ph(self, desired):
        pass

    def _soil_moisture(self, desired):
        pass

    def _air_temp(self, desired):
        pass

    def _circulation(self, desired):
        pass

    def _co2(self, desired):
        pass

    def _lighting(self, desired):
        pass

    def _humidity(self, desired):
        pass
