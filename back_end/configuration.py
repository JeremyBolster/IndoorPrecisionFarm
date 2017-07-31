import collections
import os
import yaml
import logging


class Config(object):

    # This is the default configuration object for this project
    config = collections.defaultdict()

    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)

    def configure(self, file_path: str=None) -> None:
        """
        This function loads a configuration file from disk using the specified file path or using the default one if
        none is provided.
        :param file_path: File path referring to the config file to load. This is only for overriding.
        :return: No value is returned by this function
        """
        config_file_name = os.path.join(
            os.path.dirname(__file__),
            'config.yaml')
        if file_path:
            config_file_name = os.path.abspath(file_path)

        with open(config_file_name) as f:
            Config.config = yaml.safe_load(f.read())
            self.log.debug("Configuration loaded as %s", str(Config.config))
