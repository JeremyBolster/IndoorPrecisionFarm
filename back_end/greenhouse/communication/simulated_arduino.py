import logging
from back_end.greenhouse.communication.communication import Communication
from typing import Dict, Any

device_to_generic_output = {'waterTemp': {'123': '20'},
                            'airTemp': {'123': '25'},
                            'lux': {'123': '1200'},
                            'pH': {'123': '7'},
                            'humidity': {'123': '.4'},
                            'co2': {'123': '600'}
                            }


class ArduinoSimulated(Communication):
    """
    This is the base class for communication with hardware. All other Implementations must implement these methods.
    """

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)

    def send_msg(self, device: str, msg: str) -> bool:
        return True

    def receive_msg(self, device: str) -> Dict[str, Any]:
        return device_to_generic_output[device]
