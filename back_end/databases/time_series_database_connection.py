import logging
from back_end.configuration import Config
from contextlib import contextmanager

from influxdb import InfluxDBClient


class TSDataBaseConnector(object):
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.config = Config.config
        self.host = self.config['influxdb']['host']
        self.db_name = self.config['influxdb']['db']
        self.user = self.config['influxdb']['username']
        self.password = self.config['influxdb']['password']
        self.port = self.config['influxdb']['port']

    def check_connection(self) -> None:
        # TODO this
        pass

    @contextmanager
    def __connect(self) -> None:
        # TODO this
        client = InfluxDBClient(host=self.host,
                                port=self.port,
                                username=self.user,
                                password=self.password,
                                database=self.db_name)

        client.create_database(self.db_name)

        json_body = [
            {
                "measurement": "cpu_load_short",
                "tags": {
                    "host": "server01",
                    "region": "us-west"
                },
                "time": "2009-11-10T23:00:00Z",
                "fields": {
                    "value": 0.64
                }
            }
        ]

        client.write_points(json_body)

    def send_metric(self, measurement: str, timestamp: str, fields: dict):
        pass

    def __execute(self):
        # TODO implement this
        pass


