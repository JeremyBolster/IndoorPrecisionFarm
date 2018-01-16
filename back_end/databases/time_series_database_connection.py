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
        self.client = None

    def check_connection(self) -> None:
        # TODO this
        pass

    @contextmanager
    def __connect(self) -> None:
        # TODO this
        self.client = InfluxDBClient(host=self.host,
                                     port=self.port,
                                     username=self.user,
                                     password=self.password,
                                     database=self.db_name)

        self.client.create_database(self.db_name)

    def send_metric(self, measurement: str, timestamp: str, fields: dict):
        self.__execute([
            {
                'measurement': measurement,
                'tags': {
                    'host': 'server01',
                    'region': 'us-west'
                },
                'time': timestamp,
                'fields': fields
            }
        ])

    def __execute(self, json_metric):
        self.client.write_points(json_metric)
