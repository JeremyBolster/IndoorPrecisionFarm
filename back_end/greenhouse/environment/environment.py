from back_end.configuration import Config

import logging


class Environment(object):
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.config = Config.config
        self.waterTemp = None
        self.pH = None
        self.soil_moisture = None
        self.airTemp = None
        self.circulation = None
        self.co2 = None
        self.lux = None
        self.humidity = None

    def setup(self,
              soil: bool=False,
              hydroponic: bool=False,
              water_temp: float=20,
              ph: float=7,
              soil_moisture: float=.5,
              air_temp: float=20,
              circulation: bool=False,
              co2: int=600,
              light_level: int=1000,
              humidity: float=.4) -> None:

        if soil and hydroponic:
            self.log.error('Only one of soil or hydroponic type may be specified for a given environment.')
            raise AttributeError('Only one of soil or hydroponic type may be specified for a given environment.')

        self.pH = ph
        self.airTemp = air_temp
        self.circulation = circulation
        self.co2 = co2
        self.lux = light_level
        self.humidity = humidity

        if soil:
            self.soil_moisture = soil_moisture

        if hydroponic:
            self.waterTemp = water_temp


