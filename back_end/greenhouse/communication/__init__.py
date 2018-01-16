

class OnOff(object):

    ON, OFF = 'ON', 'OFF'

    def __str__(self):
        return self.status

    def __init__(self):
        self.status = OnOff.OFF

    def is_on(self) -> bool:
        return self.status == OnOff.ON

    def is_off(self) -> bool:
        return self.status == OnOff.OFF

    def turn_on(self) -> None:
        self.status = OnOff.ON

    def turn_off(self) -> None:
        self.status = OnOff.OFF
