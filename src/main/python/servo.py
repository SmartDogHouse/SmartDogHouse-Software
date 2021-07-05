import machine
from actuator import Actuator


class Servo(Actuator):

    """Servo rotates in a range, given an angle"""
    current_angle = 0

    def __init__(self, pin_num, range_min=30, range_max=130, frequency=50):

        """ constructor.
        :param pin_num: number of pin that will command servo with PWM
        :param range_min: min angle the servo works
        :param range_max: max angle the servo works
        :param frequency: frequency PWM of servo """
        pin = machine.Pin(pin_num)
        self.servo = machine.PWM(pin, freq=frequency)
        self.range_min = range_min
        self.range_max = range_max
        self.frequency = frequency

    def __str__(self):
        """prints the object."""
        return "Servo: current angle: {}, ".format(self.current_angle)

    def angle(self, angle):
        """moves actuator to angle."""
        if self.range_min <= angle <= self.range_max:
            self.current_angle = angle
            self.servo.duty(angle)
            return True
        else:
            return False

    def get_angle(self):
        """current angle."""
        return self.current_angle
