import logging
import subprocess
import time
import os


DEFAULT_SAVE_LOCATION = 'media/webcam/'


class Webcam(object):
    """
    This is a class used to take pictures via a webcam.
    """

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)

    def take_photo(self, device: str=None, file_save_path: str=None)-> None:
        """
        This function takes a photo from the webcam.
        TODO: may have to skip frames before the picture looks decent.
        :param device:  Path to device (Not currently used)
        :param file_save_path: Path to save to file at
        :return: None
        """
        if not file_save_path:
            file_save_path = os.path.abspath(os.path.join(
                os.path.abspath(__file__),
                '../../../',
                DEFAULT_SAVE_LOCATION
            ))
        self.log.debug('Saving webcam photo to %s', file_save_path)

        subprocess.run(['fswebcam', '-r', '640x480', '--jpeg', '85', '-D', '1', str(time.time())+'.jpg'],
                       cwd=file_save_path)
