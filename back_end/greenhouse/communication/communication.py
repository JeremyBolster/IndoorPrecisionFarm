import logging
from back_end.configuration import Config
from back_end.greenhouse.communication import OnOff
from typing import Dict, List


class Communication(object):
    """
    This is the base class for communication with hardware. All other Implementations must implement these methods.
    """

    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.config = Config.config
        self.sensor_list = self.config['sensorList']

    def send_msg(self, msg: List[str]) -> bool:
        """
        This method sends a message as a command to the specified sensor. It returns a boolean representing whether it
        was successful or not.
        :param msg: Message to send to the sensor
        :return: Success status of the message
        """
        raise NotImplementedError

    def receive_msg(self, device: str) -> Dict[float, float]:
        """
        This method gets the stored messages for a given sensor from the queue.
        :param device: The device to receive messages for
        :return: The messages of a given sensor. This is a dictionary mapping from the timestamp to the 'value'
        """
        raise NotImplementedError

    def toggle_device(self, device: str, on_off: OnOff) -> bool:
        """
        This method toggles the specified device to the specified status. It returns the success of the toggle as a
        boolean.
        :param device: Name of the device to toggle as a string.
        :param on_off: Desired status of the device.
        :return: The success of the toggle.
        """
        raise NotImplementedError
