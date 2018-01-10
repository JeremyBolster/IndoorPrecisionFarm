import yaml
import time
import requests
import os
from os import path
from typing import List
from django.conf import settings

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
                 climate=consume_climate(url),
                 pattern=consume_pattern(url))
        )
        consume_image(url, farm['name'])

    Farm.last_update = time.time()
    Farm.farm_data_cache = {'farms': new_data}
    Farm.query_in_progress = False
    return Farm.farm_data_cache


def check_success(consumable: dict) -> bool:
    if 'success' in consumable and consumable['success']:  # Check that the message was received successfully
        return True
    else:
        return False


def consume_image(url: str, farm_name: str) -> bool:
    """
    This method consumes an image from a farm.
    :param url: The base url of the farm to query.
    :param farm_name: The name of the farm whos image is to be consumed
    :return: The name of the file which was saved to MEDIA_ROOT
    """
    # TODO this should check the last time an image was grabbed and only grab a new one if it was changed.
    consumable = requests.get(url + '/api/v1/image').json()
    if not check_success(consumable):
        return False

    image_url = consumable['image_url']
    last_updated = consumable['last_updated']

    output_filepath = path.abspath(path.dirname(path.realpath(__file__)) +
                                   '/media/' + farm_name.replace(' ', '_') + '-view.jpg')

    response = requests.get(url + image_url)
    with open(output_filepath, 'wb') as out_file:
        out_file.write(response.content)

    return True


def consume_pattern(url: str) -> dict:
    consumable = requests.get(url + '/api/v1/pattern/').json()
    if check_success(consumable):
        message = consumable['message']
        return message
    else:
        raise AttributeError('Message was not received successfully')


def consume_status(url: str) -> dict:
    consumable = requests.get(url + '/api/v1/status/').json()
    if check_success(consumable):
        message = consumable['message']
        return message
    else:
        raise AttributeError('Message was not received successfully')


def consume_climate(url: str) -> dict:
    consumable = requests.get(url + '/api/v1/climate/').json()
    if check_success(consumable):
        message = consumable['message']
        return message
    else:
        raise AttributeError('Message was not received successfully')


def load_config() -> None:
    with open(
            path.abspath(
                path.join(
                    path.dirname(path.realpath(__file__)),
                    'farm_config.yaml'))) as f:
        Farm.farm_data = yaml.safe_load(f)


def get_list_of_patterns() -> List[str]:
    return os.listdir(
        path.join(settings.MEDIA_ROOT,
                  'climate_patterns'))


def update_pattern_offset(url_root, offset) -> bool:
    return requests.post(url=url_root + '/api/v1/status/', json={'time_offset': offset}).ok


def change_climate_pattern(url_root:str, pattern_name: str) -> bool:
    if '/' in pattern_name:
        return False # Evil file name!!!
    pattern_name_semi_clean = pattern_name.split('.')[0] + '.yaml'
    # The above is a sad attempt to scrub the file name to prevent ../../../ shenanigans

    pattern_path = path.join(settings.MEDIA_ROOT,
                             'climate_patterns',
                             pattern_name_semi_clean)
    pattern = None
    with open(pattern_path) as f:
        pattern = yaml.safe_load(f.read())

    if not pattern:
        return False

    return requests.post(url=url_root + '/api/v1/pattern/', json=pattern).ok


def update_farm(request_query) -> bool:
    farm_url = request_query['farm_url']
    if 'pattern_offset' in request_query:
        return update_pattern_offset(farm_url, request_query['pattern_offset'])
    elif 'climate_pattern_name' in request_query:
        return change_climate_pattern(farm_url, request_query['climate_pattern_name'])
    else:
        return False
