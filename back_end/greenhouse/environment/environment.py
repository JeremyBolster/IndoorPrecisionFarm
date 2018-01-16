from back_end.configuration import Config
import logging


class Environment(object):
    """
    This class is a data structure. The main purpose of this class is to encapsulate an environmental state.
    This state can be either physical or virtual.
    """
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.config = Config.config
        self.current_time = 0
        self.values = dict(
            water_temp=None,
            pH=None,
            soil_moisture=None,
            air_temp=None,
            co2=None,
            lux=None,
            humidity=None,

            air_heater=None,
            air_cooler=None,
            water_heater=None,
            water_cooler=None,
            ph_up=None,
            ph_down=None,
            water_soil=None,
            circulation_fan=None,
            increase_c02=None,
            lights=None,
            humidifier=None,
            dehumidifier=None
        )

    def __str__(self):
        return str(self.to_json())

    def to_json(self):
        output = {}
        for item, value in self.values.items():
            if value:
                output.setdefault(item, value)
        if self.current_time:
            output['current_time'] = int(self.current_time)
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

        self.values['pH'] = ph
        self.values['air_temp'] = air_temp
        self.values['circulation'] = circulation
        self.values['co2'] = co2
        self.values['lux'] = light_level
        self.values['humidity'] = humidity

        if soil:
            self.values['soil_moisture'] = soil_moisture

        if hydroponic:
            self.values['water_temp'] = water_temp

    def update(self, pattern: dict)-> None:
        for key, value in pattern.items():

            # Hard-coding for compatibility with MIT Food Computer Recipes
            if key in 'waterTemp':
                self.values['water_temp'] = value
                continue
            if key in 'airTemp':
                self.values['air_temp'] = value
                continue
            self.values[key] = value
