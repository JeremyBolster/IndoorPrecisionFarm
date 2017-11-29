import yaml
import time
import requests
from os import path

CACHE_TIMEOUT = 5  # cache refresh timeout in seconds


class Farm(object):
    
    farm_data = []
    farm_data_cache = {}
    last_update = time.time()
    query_in_progress = False

    def __init__(self):
        pass
    

def query_farms() -> dict:
    # first we load the farm configs if they have not already been loaded
    if not Farm.farm_data:
        load_config()
        
    # Time to update the cache
    if time.time() < Farm.last_update + CACHE_TIMEOUT or Farm.query_in_progress:
        return Farm.farm_data_cache

    Farm.query_in_progress = True
    new_data = []
    for farm in Farm.farm_data:
        # {'name': 'Test Farm 1', 'url': 'http://127.0.0.1:8001'}
        url = farm['url']
        new_data.append(
            dict(name=farm['name'],
                 url=url,
                 status=consume_status(url),
                 climate=consume_climate(url))
        )

    Farm.last_update = time.time()
    Farm.farm_data_cache = {'farms': new_data}
    Farm.query_in_progress = False
    return Farm.farm_data_cache

    
def check_success(consumable: dict) -> bool:
    if 'success' in consumable and consumable['success']:  # Check that the message was received successfully
        return True
    else:
        return False


def consume_image(url: str) -> str:
    """
    This method consumes an image from a farm.
    :param url: The base url of the farm to query.
    :return: The name of the file which was saved to MEDIA_ROOT
    """
    # TODO this should check the last time an image was grabbed and only grab a new one if it was changed.
    # TODO implement basic functionality
    consumable = requests.get(url + '/api/v1/image').json()
    return ''



def consume_status(url: str) -> dict:
    consumable = requests.get(url + '/api/v1/status').json()
    if check_success(consumable):
        message = consumable['message']
        return message
    else:
        raise AttributeError('Message was not received successfully')
    # {
    #     message: {
    #         desired state: {
    #     water_temp: 24,
    #     pH: 6,
    #     air_temp: 25,
    #     co2: 1000,
    #     lux: 1200,
    #     humidity: 45
    # },
    #     elapsed time: 15.006081104278564
    # },
    # success: true
    # }
    pass


def consume_climate(url: str) -> dict:
    consumable = requests.get(url+'/api/v1/climate').json()
    if check_success(consumable):
        message = consumable['message']
        message['last_resolved'] = int(time.time() - message['current_time'])
        # gives us the time difference between now and when the farm was last updated
        return message
    else:
        raise AttributeError('Message was not received successfully')

    # {
    #     message: {
    #         water_temp: 20,
    #         pH: 7,
    #         air_temp: 25,
    #         co2: 600,
    #         lux: 1200,
    #         humidity: 0.4,
    #         air_heater: "OFF",
    #         air_cooler: "OFF",
    #         water_heater: "ON",
    #         water_cooler: "OFF",
    #         ph_up: "OFF",
    #         ph_down: "ON",
    #         water_soil: "OFF",
    #         circulation_fan: "OFF",
    #         increase_c02: "ON",
    #         lights: "ON",
    #         humidifier: "ON",
    #         dehumidifier: "OFF"
    #     },
    #     success: true
    # }
        
        
def load_config() -> None:
    with open(
        path.abspath(
            path.join(
                path.dirname(path.realpath(__file__)),
                'farm_config.yaml'))) as f:
        Farm.farm_data = yaml.safe_load(f)