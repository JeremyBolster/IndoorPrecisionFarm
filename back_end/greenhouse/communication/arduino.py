import logging
import PyCmdMessenger
import collections
import time
import threading
from threading import Thread
from typing import Dict, Any
from back_end.greenhouse.communication.communication import Communication
from back_end.configuration import Config

POLL_INTERVAL = 30  # poll interval for each sensor in seconds


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

    def initialize_arduino(self):
        # TODO error checking
        # TODO auto-detect arduino
        arduino = PyCmdMessenger.ArduinoBoard(Config.config['communication']['arduinoDevice'], baud_rate=9600)
        self.cmd = PyCmdMessenger.CmdMessenger(arduino, Config.config['communication']['arduinoCommands'])
        th = Thread(target=self._poll_sensors)
        th.daemon = True
        th.start()

    def send_msg(self, sensor: str, msg: str) -> bool:
        """
        This method sends a message as a command to the specified sensor. It returns a boolean representing whether it
        was successful or not.
        :param sensor: Name of the sensor
        :param msg: Message to send to the sensor
        :return: Success status of the message
        """
        with self.lock:
            self.cmd.send(sensor, msg)
            return_msg = self.cmd.receive()
        assert return_msg[1][0] == msg
        # TODO something smarter with this in case of error
        return 'success' == return_msg[1][1]

    def receive_msg(self, device: str) -> Dict[str, Any]:
        """
        This method gets the stored messages for a given sensor from the queue.
        :param device: The device to recieve messages for
        :return: The messages of a given sensor. This is a dictionary mapping from the timestamp to the 'value'
        """
        with self.lock:
            messages = self.devices['device']
            self.devices['device'] = {}
        return messages

    def _poll_sensors(self):
        self.log.debug('Beginning sensor poll loop in daemonized thread.')
        time.sleep(POLL_INTERVAL)
        while True:
            time.sleep(POLL_INTERVAL / len(self.sensor_list))
            with self.lock:
                msg = self.cmd.receive()
            self.log.log(5, 'Received message from Arduino: %s', str(msg))
            message_type = msg[0]
            device = msg[1][0]
            value = msg[1][1]
            time_recieved = msg[2]

            if message_type not in 'sensorValue':
                # TODO do something more sensible with this error
                self.log.error('Bad message type received by sensor polling util. %s', message_type)
                raise AttributeError

            if device in 'null':
                return
            with self.lock:
                device = self.devices['device']
                device.extend({time_recieved: value})
