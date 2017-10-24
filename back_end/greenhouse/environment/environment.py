from back_end.configuration import Config
from back_end.greenhouse.communication.communication import ON, OFF

import logging


class Environment(object):
    """
    This class is a data structure. The main purpose of this class is to encapsulate an environmental state. This state
    can be either physical or virtual.
    """
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.config = Config.config
        self.water_temp = None
        self.pH = None
        self.soil_moisture = None
        self.air_temp = None
        self.co2 = None
        self.lux = None
        self.humidity = None

        self.humidifier = OFF
        self.light = OFF
        self.heater = OFF
        self.air_conditioner = OFF
        self.circulation = OFF

    def __str__(self):
        return str(self.to_json())

    def to_json(self):
        output = {}
        for item, value in self.__dict__.items():
            if value:
                output.setdefault(item, value)
        return output

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
        self.air_temp = air_temp
        self.circulation = circulation
        self.co2 = co2
        self.lux = light_level
        self.humidity = humidity

        if soil:
            self.soil_moisture = soil_moisture

        if hydroponic:
            self.water_temp = water_temp

    def update(self, pattern: dict)-> None:
        for key, value in pattern.items():

            # Hard-coding for compatability with MIT Food Computer Recipes
            if key in 'waterTemp':
                self.water_temp = value
                continue
            if key in 'airTemp':
                self.air_temp = value
                continue
            self.__setattr__(key, value)
            self.soil_moisture = None
            self.circulation = None

