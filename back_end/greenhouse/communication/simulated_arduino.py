import logging
from back_end.greenhouse.communication.communication import Communication

device_to_generic_output = {'water_temp': 20,
                            'air_temp': 25,
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

    def receive_msg(self, device: str) -> dict:
        pass
