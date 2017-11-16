from back_end.configuration import Config
from back_end.databases.time_series_database_connection import TSDataBaseConnector
from back_end.greenhouse.communication.communication import Communication
from back_end.greenhouse.environment.environment import Environment
from back_end.greenhouse.environment.environmental_control import EnvironmentalControl
from threading import Thread
import time
import logging
import yaml
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Greenhouse(object, metaclass=Singleton):
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
        self.sensors = None
        self.desired_state = None
        self.current_state = None
        self.remote_data_store = None
        self.pattern = None
        self.control = None
        self.running = False
        self.start_time = 0
        self.time_offset = 0
        self.elapsed_time = 0

    def setup(self, sensors: Communication, climate_pattern: str, remote_store: TSDataBaseConnector=None) -> None:
        """
        This method sets the values of the greenhouse.
        :param sensors: The device that represents the sensors and devices of the physical greenhouse.
        :param climate_pattern: A file of a climate pattern to load and execute.
        :param remote_store: The remote database to push metrics to.
        :return:
        """
        self.sensors = sensors
        self.current_state = Environment()
        self.desired_state = Environment()
        self.remote_data_store = remote_store
        climate_file_name = os.path.join(
            os.path.dirname(__file__),
            os.path.pardir,
            'default_climate.yaml')
        if climate_pattern:
            climate_file_name = os.path.abspath(climate_pattern)
        with open(climate_file_name) as f:
            self.pattern = yaml.safe_load(f.read())
        # TODO set the current state of the greenhouse to the desired state at the beginning
        self.control: EnvironmentalControl = EnvironmentalControl(self.sensors, self.current_state)

    def run(self) -> None:
        """
        This function runs the current pattern in the greenhouse. It runs this in a daemonized thread.
        """
        if self.running:
            return
        self.running = True
        th = Thread(target=self._runnable)
        th.daemon = True
        th.start()

    def _runnable(self):
        """
        This function runs the current pattern in the greenhouse. This function should not be called from the main
        thread
        :return:
        """
        self.log.info('Running greenhouse')
        self.start_time = time.time()
        # TODO loop to create a new desired state of the greenhouse
        # TODO loop to update the environmental_control class with the new desired state of the greenhouse
        while True:
            time.sleep(15)  # TODO this is hacky
            self._get_sensor_data()
            self._update_desired_state()

    def _update_desired_state(self):
        # TODO make this update the actual state of the greenhouse
        try:
            pattern = self._get_current_params()
        except IndexError:
            # TODO this means the farm has finished processing the pattern
            # Not sure what to do here
            self.log.warning('The farm has finished executing the current pattern')
        self.log.debug("At time: %s , The current pattern is: %s",
                       time.time() - self.start_time + self.time_offset,
                       pattern)
        self.desired_state.update(pattern)
        # self.log.debug("The desired state is now set as: %s", self.desired_state)
        self.control.set_environment(self.desired_state)

    def _get_current_params(self):
        # self.pattern['operations'] is the actual grow parameters
        # it is a list of 'stages' of growth parameters

        self.elapsed_time = time.time() - self.start_time + self.time_offset
        DAY, NIGHT = 'day', 'night'
        current_stage = 0
        current_cycle = 0
        current_day_night = DAY

        end_time_of_cycle = 0
        while self.elapsed_time > end_time_of_cycle:
            end_time_of_cycle += self.pattern['operations'][current_stage][current_day_night]['hours'] * 3600
            # 3600 for hours to seconds conversion
            if self.elapsed_time <= end_time_of_cycle:
                return self.pattern['operations'][current_stage][current_day_night]['environment']

            # Alternate between day and night
            if current_day_night in DAY:
                current_day_night = NIGHT
            else:
                current_day_night = DAY
                current_cycle += 1

            # Skip to the next stage if the current has already completed all of its cycles
            if current_cycle == self.pattern['operations'][current_stage]['cycles']:
                current_cycle = 0
                current_stage += 1

    def _get_sensor_data(self):
        for sensor in self.config['sensorList']:
            new_statues = self.sensors.receive_msg(sensor)
            newest_timestamp = 0
            for timestamp, status in new_statues.items():
                self._push_state(sensor, timestamp, status)
                if int(timestamp) > int(newest_timestamp):
                    newest_timestamp = timestamp
            if newest_timestamp:  # This checks if there even is a newer timestamp
                self.current_state.values[sensor] = float(new_statues[newest_timestamp])

        self.log.debug("The current state of the farm is: %s", self.current_state)

    # TODO this
    def _push_state(self, sensor: str, timestamp: str, status: str):
        if not self.remote_data_store:
            # self.log.debug('(Faux) Pushed %s at %s with a value of %s', sensor, timestamp, status)
            return
        self.remote_data_store.send_metric(sensor, timestamp, status)
