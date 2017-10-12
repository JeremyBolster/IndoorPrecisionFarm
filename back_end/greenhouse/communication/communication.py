import logging
from back_end.configuration import Config
from typing import Dict, Any

ON, OFF = 'ON', 'OFF'


class Communication(object):
    """
    This is the base class for communication with hardware. All other Implementations must implement these methods.
    """

    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.config = Config.config
        self.sensor_list = self.config['sensorList']

    def send_msg(self, device: str, msg: str) -> bool:
        raise NotImplementedError

    def receive_msg(self, device: str) -> Dict[float, float]:
        raise NotImplementedError
