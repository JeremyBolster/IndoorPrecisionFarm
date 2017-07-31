from back_end.configuration import Config
from back_end.database_connection import DataBaseConnector
from back_end.log import GreenHouseLog


def parse_args():
    """ This function parses the command line arguments and verifies that they
    are set sanely. """
    pass


if __name__ == '__main__':
    parse_args()
    Config().configure()
    GreenHouseLog().set_up_loggers(stderr=True)
    DataBaseConnector().check_connection()


