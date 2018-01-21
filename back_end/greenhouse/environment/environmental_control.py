from back_end.configuration import Config
from back_end.greenhouse.communication import OnOff
from back_end.greenhouse.communication.communication import Communication
from back_end.greenhouse.environment.environment import Environment

import logging
import time
import threading
from threading import Thread


REFRESH_INTERVAL = 10


class EnvironmentalControl(object):
    def __init__(self, farm: Communication, status: Environment):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.config = Config.config
        self.farm = farm
        self.farm_status = status
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
        This function safely updates the reference to the most recent sensor values from the farm.
        :param desired_environment: A desired environment to create
        """
        with self.lock:
            self.desired_environment = desired_environment

    def _set_environment(self) -> None:
        """
        This function is an infinite loop runnable to continue toggling the farm's devices to always try and meet the
        desired environmental state.
        """
        last_update_time = time.time()
        while True:
            # The 'math' in the next line keeps the refresh intervals more regular since the update takes time to
            # complete.
            time.sleep(REFRESH_INTERVAL - (time.time() - last_update_time))  # REFRESH_INTERVAL - ELAPSED_TIME
            last_update_time = time.time()
            with self.lock:
                if self.desired_environment:
                    self._update_environment(self.desired_environment)

    def _update_environment(self, environment: Environment) -> None:
        """
        This is a function that takes the current desired environment and applies it to this objects assigned farm.
        :param environment: The desired environment
        """
        e_vals, f_vals = environment.values, self.farm_status.values

        self._generic_update(e_vals, f_vals, 'water_temp', 'water_heater', 'water_cooler')  # only works if hydroponic
        self._generic_update(e_vals, f_vals, 'pH', 'ph_up', 'ph_down')  # Handles either soil or water ph
        self._generic_update(e_vals, f_vals, 'air_temp', 'air_heater', 'air_cooler')
        self._generic_update(e_vals, f_vals, 'co2', 'co2_up', 'co2_down')
        self._generic_update(e_vals, f_vals, 'humidity', 'humidifier', 'dehumidifier')
        self._generic_update(e_vals, f_vals, 'soil_moisture', 'water_soil', None)  # only works if soil based

        self._always_set(environment.values['circulation_fan'], 'circulation_fan')
        self._always_set(environment.values['lux'], 'lights')

    def _generic_update(self, desired, current, name, increase_device_name, decrease_device_name=None) -> None:
        increase, decrease = self._on_off(current[name], desired[name])
        self.farm.toggle_device(increase_device_name, increase)
        self.farm_status.values[increase_device_name] = str(increase)
        if decrease_device_name:
            self.farm.toggle_device(decrease_device_name, decrease)
            self.farm_status.values[decrease_device_name] = str(decrease)

    def _always_set(self, desired, device_name) -> None:
        status = OnOff()
        if desired:
            status.turn_on()
        self.farm.toggle_device(device_name, status)
        self.farm_status.values[device_name] = str(status)

    @staticmethod
    def _on_off(current, desired):
        one = OnOff()
        two = OnOff()
        if not current or not desired:
            # This covers the issue of certain values not being implemented.
            return one, two
        if current < desired:  # TODO add tolerance
            one.turn_on()
        elif current > desired:  # TODO add tolerance
            two.turn_on()
        return one, two
