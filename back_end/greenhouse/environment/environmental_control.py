from back_end.configuration import Config
from back_end.greenhouse.communication.communication import Communication, ON, OFF
from back_end.greenhouse.environment.environment import Environment

import threading
from threading import Thread

import logging
import time

REFRESH_INTERVAL = 10


class EnvironmentalControl(object):
    def __init__(self, greenhouse: Communication, status: Environment):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.config = Config.config
        self.greenhouse = greenhouse
        self.greenhouse_status = status
        self.desired_environment = None
        self.lock = threading.Lock()
        self.thread = self.set_up_thread()

    def set_up_thread(self) -> Thread:
        th = Thread(target=self._set_environment)
        th.daemon = True
        th.start()
        return th

    def set_environment(self, desired_environment: Environment) -> None:
        """
        This is the main function of this class. This function takes a given environment and applies it to its assigned
        communication device / greenhouse.
        :param desired_environment: A desired environment to create
        :return: None
        """
        with self.lock:
            self.desired_environment = desired_environment

    def _set_environment(self) -> None:
        """
        This function updates the environment to whatever value is
        :return: None
        """
        while True:
            time.sleep(REFRESH_INTERVAL)
            th = Thread()
            with self.lock:
                if self.desired_environment:
                    # By passing environment as a reference we can let this call be threaded, thus releasing the lock
                    th = Thread(target=self._update_environment, args=[self.desired_environment])
            th.daemon = True
            th.start()
            th.join()

    def _update_environment(self, environment: Environment) -> None:
        """
        This is a function that takes the current desired environment and applies it to this objects assigned
        greenhouse.
        :param environment: The desired environment
        :return: None
        """
        self._water_temp(environment.values['water_temp'])  # only works if hydroponic
        self._ph(environment.values['pH'])  # Handles either soil or water ph
        self._soil_moisture(environment.values['soil_moisture'])  # only works if soil based
        self._air_temp(environment.values['air_temp'])
        self._circulation(environment.values['circulation'])
        self._co2(environment.values['co2'])
        self._lighting(environment.values['lux'])
        self._humidity(environment.values['humidity'])

    def _water_temp(self, desired):
        current = self.greenhouse_status.values['water_temp']
        water_heater, water_cooler = self._on_off(current, desired)
        self.greenhouse.toggle_device('water_heater', water_heater)
        self.greenhouse.toggle_device('water_cooler', water_cooler)

    def _ph(self, desired):
        current = self.greenhouse_status.values['pH']
        ph_up, ph_down = self._on_off(current, desired)
        self.greenhouse.toggle_device('ph_up', ph_up)
        self.greenhouse.toggle_device('ph_down', ph_down)

    def _soil_moisture(self, desired):
        current = self.greenhouse_status.values['soil_moisture']
        water, _ = self._on_off(current, desired)
        self.greenhouse.toggle_device('water_soil', water)

    def _air_temp(self, desired):
        current = self.greenhouse_status.values['air_temp']
        air_heater, air_cooler = self._on_off(current, desired)
        self.greenhouse.toggle_device('air_heater', air_heater)
        self.greenhouse.toggle_device('air_cooler', air_cooler)

    def _circulation(self, desired):
        if desired:
            self.greenhouse.toggle_device('circulation_fan', ON)
        else:
            self.greenhouse.toggle_device('circulation_fan', OFF)

    def _co2(self, desired):
        current = self.greenhouse_status.values['co2']
        co2, _ = self._on_off(current, desired)
        self.greenhouse.toggle_device('increase_c02', co2)

    def _lighting(self, desired):
        lights = OFF
        if desired:
            lights = ON
        self.greenhouse.toggle_device('lights', lights)

    def _humidity(self, desired):
        current = self.greenhouse_status.values['humidity']
        humidifier, dehumidifier = self._on_off(current, desired)
        self.greenhouse.toggle_device('humidifier', humidifier)
        self.greenhouse.toggle_device('dehumidifier', dehumidifier)

    @staticmethod
    def _on_off(current, desired):
        if not current or not desired:
            # This covers the issue of certain values not being implemented.
            return OFF, OFF
        one = OFF
        two = OFF
        if current < desired:  # TODO add tolerance
            one = ON
        elif current > desired:  # TODO add tolerance
            two = ON
        return one, two
