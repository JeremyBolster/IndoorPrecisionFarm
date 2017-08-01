import logging
import sys
from colorlog import ColoredFormatter
from logging.handlers import RotatingFileHandler

LOG_FORMAT = '%(asctime)s %(log_color)s%(levelname)-8s%(reset)s | %(name)20s | %(filename)25s %(lineno)3s | %(log_color)s%(message)s%(reset)s'
formatter = ColoredFormatter(fmt=LOG_FORMAT, datefmt='%H:%M:%S')
logging.VERBOSE = 1
logging.addLevelName(logging.VERBOSE, 'VERBOSE')
logging.Logger.verbose = lambda inst, msg, *args, **kwargs: inst.log(logging.VERBOSE, msg, *args, **kwargs)
logging.verbose = lambda msg, *args, **kwargs: logging.log(logging.VERBOSE, msg, *args, **kwargs)


class GreenHouseLog(object):
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)

    def set_up_loggers(self,
                       file_path: str='./greenhouse.log', stderr: bool=False, log_level: int=logging.DEBUG) -> None:
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

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
