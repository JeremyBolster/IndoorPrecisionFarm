#! /usr/env python3
import argparse
import os
import json

config = None

if __name__ == __main__:
    parse_args()
    config()
    # It would be nice if this was the first thing called but the log file will
    # be defined in the configuration function.
    init_logs()
    run()


def init_logs():
    """This function initializes the logging for the entire application. This
    function calls an external function from log.py to do the heavy lifting. """
    pass


def parse_args():
    """ This function parses the command line arguments and verifies that they
    are set sanely. """
    pass


def run():
    """ The purpose of this function is to start running an instance of the
    greenhouse application. """
    # TODO Fill this in
    pass


def config():
    """ The purpose of this function is to set values in the configuration
    object. This overrides the values in the configuration file to allow
    easy modification on the command line or via scripting. """
    # TODO Fix this method to actually work properly

    # TODO fix this file path
    config_file_name = os.path.join(os.path.abs(os.path(this.__file__)),
                    'config.json')
    config = {}
    with open(config_file_name) as f:
        config = json.loads(f)
