from servo import Servo
from actuator import Actuator


class Valve(Actuator):

    """Valve opens and closes"""

    opened = True

    def __init__(self, pin_num, initial_opened=True):

        """ constructor.
        :param pin_num: number of pin that will command valve with PWM
        :param initial_opened: if it has to be open at the beginning
        """
        self.servo = Servo(pin_num)
        self.opened = initial_opened
        if initial_opened:
            self.open()
        else:
            self.close()

    def __str__(self):
        """prints the object."""
        return "Valve: current status: {}. ".format(self.status())

    def open(self):
        self.servo.angle(30)
        self.opened = True

    def close(self):
        self.servo.angle(120)
        self.opened = False

    def switch(self):
        """changes the status of the valve, returns true if opened, false if closed."""
        if self.opened:
            self.close()
        else:
            self.open()
        return self.opened

    def is_open(self):
        """if the valve is currently open."""
        return self.opened

    def is_closed(self):
        """if the valve is currently closed."""
        return not self.is_open()

    def status(self):
        """if the valve is currently opened or closed."""
        if self.opened:
            return "opened"
        else:
            return "closed"
