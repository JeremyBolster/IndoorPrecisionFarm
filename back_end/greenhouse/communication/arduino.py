import logging
import PyCmdMessenger
import collections
import time
import threading
from threading import Thread
from typing import Dict, List, Any
from back_end.greenhouse.communication import OnOff
from back_end.greenhouse.communication.communication import Communication
from back_end.configuration import Config
from serial.tools import list_ports

POLL_INTERVAL = 15  # poll interval for each sensor in seconds
ARDUINO_ID = 'Arduino'
SUCCESS, FAILURE = True, False


class Arduino(Communication):
    """
    This is a class used to connect to an Arduino for communication to sensors.
    """
    lock = threading.Lock()

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.cmd = None
        self.devices = collections.defaultdict(lambda: {})
        self.config = Config.config['communication']
        self.initialize_arduino()

    def initialize_arduino(self):
        # TODO error checking
        arduino = PyCmdMessenger.ArduinoBoard(self.find_arduino(), baud_rate=9600)
        self.cmd = PyCmdMessenger.CmdMessenger(arduino, self.config['arduinoCommands'])
        th = Thread(target=self._poll_sensors)
        th.daemon = True
        th.start()

    def find_arduino(self, hwid: str = None) -> str:
        arduinos = [
            p.device
            for p in list_ports.comports()
            if ARDUINO_ID in p.description
        ]
        if not arduinos:
            self.log.error('No Arduinos were found.')
            raise IOError('No Arduino detected')

        if len(arduinos) > 1 and not hwid:
            self.log.error('Multiple arduinos found and not unique ID specified. Dumping found Arduinos and failing.')
            for ard in arduinos:
                self.log.info(
                    "Device: %s , Name: %s , Description: %s , HWID: %s , VID: %s , PID: %s , Serial No.: %s " %
                    ard.device, ard.name, ard.description, ard.hwid, ard.vid, ard.pid, ard.serial_number)
            raise IOError('Cannot determine which Arduino to ues. Failing.')

        return arduinos[0]

    def toggle_device(self, device: str, on_off: OnOff) -> bool:
        """
        This method toggles the specified device to the specified status. It returns the success of the toggle as a
        boolean.
        :param device: Name of the device to toggle as a string.
        :param on_off: Desired status of the device.
        :return: The success of the toggle.
        """
        device_pin = self.config['devicePins'][device]
        return self.send_msg(['toggleDevice', device_pin, on_off.is_on()])

    def send_msg(self, msg: List[Any]) -> bool:
        """
        This method sends a message as a command to the specified sensor. It returns a boolean representing whether it
        was successful or not.
        :param msg: Message to send to the sensor
        :return: Success status of the message
        """
        with self.lock:
            self.cmd.send(*msg)
        return True

    def receive_msg(self, device: str) -> Dict[float, float]:
        """
        This method gets the stored messages for a given sensor from the queue.
        :param device: The device to receive messages for
        :return: The messages of a given sensor. This is a dictionary mapping from the timestamp to the 'value'
        """
        with self.lock:
            messages = self.devices[device]
            self.devices[device] = {}
        return messages

    def _poll_sensors(self):
        self.log.debug('Beginning sensor poll loop in daemonized thread.')
        time.sleep(POLL_INTERVAL)
        while True:
            time.sleep(POLL_INTERVAL / len(self.sensor_list))
            with self.lock:
                self.cmd.send('poll')
            time.sleep(1)  # TODO this is hacky
            while self._receive_sensor_poll():
                continue

    def _receive_sensor_poll(self)->bool:
        with self.lock:
            msg = self.cmd.receive()
        try:
            if msg:
                self.log.log(5, 'Received message from Arduino: %s', str(msg))
                message_type = msg[0]
                device = msg[1][0]
                value = msg[1][1]
                time_received = msg[2]

                if message_type not in 'sensorValue':
                    # TODO do something more sensible with this error
                    self.log.error('Bad message type received by sensor polling util. %s', message_type)
                    raise AttributeError

                if device in 'null':
                    return FAILURE
                with self.lock:
                    device_values = self.devices[device]
                    device_values[time_received] = value
                    return SUCCESS
            else:
                return FAILURE
        except Exception:
            self.log.debug("Message received was unexpected: %s", msg)
            return FAILURE
