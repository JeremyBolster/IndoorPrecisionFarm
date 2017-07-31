import logging
import sys
from colorlog import ColoredFormatter

LOG_FORMAT = '%(asctime)s %(log_color)s%(levelname)-8s%(reset)s | %(name)20s | %(log_color)s%(message)s%(reset)s'
formatter = ColoredFormatter(fmt=LOG_FORMAT, datefmt='%H:%M:%S')


class GreenHouseLog(object):
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)

    def set_up_loggers(self,
                       file_path: str='./greenhouse.log', stderr: bool=False, log_level: int=logging.DEBUG) -> None:
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        fh = logging.FileHandler(file_path)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        root.addHandler(fh)

        if stderr:
            ch = logging.StreamHandler(sys.stderr)
            ch.setLevel(log_level)
            ch.setFormatter(formatter)
            root.addHandler(ch)
