import logging
import sys
from colorlog import ColoredFormatter
from logging.handlers import RotatingFileHandler

COLOR_LOG_FORMAT = '%(asctime)s %(log_color)s%(levelname)-8s%(reset)s | %(name)20s | %(filename)25s %(lineno)3s | %(log_color)s%(message)s%(reset)s'
LOG_FORMAT = '%(asctime)s %(levelname)-8s | %(name)20s | %(filename)25s %(lineno)3s | %(message)s'
formatter = ColoredFormatter(fmt=COLOR_LOG_FORMAT, datefmt='%H:%M:%S')


class GreenHouseLog(object):
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)

    def set_up_loggers(self, file_path: str, stderr: bool, log_level: int=logging.DEBUG) -> None:
        root = logging.getLogger()
        root.setLevel(log_level)

        # Max Bytes is set to 10MB ((2**20)*10)
        fh = RotatingFileHandler(file_path, maxBytes=10485760, backupCount=5)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        root.addHandler(fh)

        if stderr:
            ch = logging.StreamHandler(sys.stderr)
            ch.setLevel(log_level)
            ch.setFormatter(formatter)
            root.addHandler(ch)
