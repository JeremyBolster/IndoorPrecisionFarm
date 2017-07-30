import collections
import os
import yaml


class Config(object):

    config = collections.defaultdict()

    def __init__(self):
        pass


def configure(file_path: str=None) -> None:
    """
    This function loads a configuration file from disk using the specified file path or using the default one if
    none is provided.
    :param file_path: File path refering to the config file to load.
    :return: No value is returned by this function
    """
    config_file_name = os.path.join(
        os.path.dirname(__file__),
        'config.json')
    if file_path:
        config_file_name = os.path.abspath(file_path)

    with open(config_file_name) as f:
        Config.config = yaml.safe_load(f.read)
