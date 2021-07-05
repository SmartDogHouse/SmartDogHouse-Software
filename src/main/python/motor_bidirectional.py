import machine
from motor import Motor


class MotorBidirectional(Motor):

    """ Motor DC rotates in one or the other direction with current, it can be inverted,
    it's basically mandatory to use a H-Bridge, a pin (0,04 A) doesn't have enough Ampere to move a motor"""

    def __init__(self, pin1_num, pin2_num, direction=1, running=False):
        """ constructor.
        :param pin1_num: number of pin that will give power or be ground
        :param pin2_num: number of pin that will give power or be ground
        :param direction: which pin should give current, can be 1 or 2
        :param running: the initial condition of the motor
        """
        self.pin1_num = pin1_num
        self.pin2_num = pin2_num
        self.direction = direction
        self.running = running
        if running:
            self.on()

    def __str__(self):
        """prints the object."""
        return "Motor bidirectional currently is running: {}, direction: {}".format(self.running, self.direction)

    def on_pin(self, pin_num):
        """Turns on given pin and off the other."""
        # for safety off-everything
        self.off()
        # turning on only one pin
        self.running = True
        if pin_num == self.pin1_num:
            self.direction = 1
            # pin 2 input
            pin2 = machine.Pin(self.pin2_num, machine.Pin.OUT)
            pin2.off()
            # on pin1
            pin1 = machine.Pin(self.pin1_num, machine.Pin.OUT)
            pin1.on()
        if pin_num == self.pin2_num:
            self.direction = 2
            # pin 1 input
            pin1 = machine.Pin(self.pin1_num, machine.Pin.OUT)
            pin1.off()
            # on pin2
            pin2 = machine.Pin(self.pin2_num, machine.Pin.OUT)
            pin2.on()

    def on_direction(self, direct):
        """starts motor in direction specified."""
        if direct == 1:
            self.on_pin(self.pin1_num)
        elif direct == 2:
            self.on_pin(self.pin2_num)

    def on(self):
        """starts motor, in direction memorized."""
        self.on_direction(self.direction)

    def on_direction_opposite(self):
        """starts motor in the opposite direction."""
        if self.direction == 1:
            self.on_direction(2)
        elif self.direction == 2:
            self.on_direction(1)

    def off(self):
        """stops motor."""
        self.running = False
        pin1 = machine.Pin(self.pin1_num, machine.Pin.OUT)
        pin1.off()
        pin2 = machine.Pin(self.pin2_num, machine.Pin.OUT)
        pin2.off()

    def get_direction(self):
        """the direction selected."""
        return self.direction
