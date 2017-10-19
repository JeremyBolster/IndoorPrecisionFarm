from back_end.greenhouse.environment.environment import Environment
from back_end.greenhouse.communication.communication import ON, OFF
import logging


class EnvironmentGoal(Environment):

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        self.light = OFF

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
