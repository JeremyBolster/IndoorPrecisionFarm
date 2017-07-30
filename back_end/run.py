#! /usr/env python3
from back_end.configuration import Config


def init_logs():
    """This function initializes the logging for the entire application. This
    function calls an external function from log.py to do the heavy lifting. """
    pass


def parse_args():
    """ This function parses the command line arguments and verifies that they
    are set sanely. """
    pass


if __name__ == __main__:
    parse_args()
    Config.configure()
    init_logs()

    pass


