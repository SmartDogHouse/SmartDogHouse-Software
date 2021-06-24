import machine


class MotorBidirectional:
    """ Motor DC rotates in one or the other direction with current, it can be inverted """

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
        """ prints the object """
        return "Motor bidirectional currently is running: {}, direction: {}".format(self.running, self.direction)

    def on_pin(self, pin_num):
        """ turns on given pin and off the other """
        # for safety off-everything
        self.off()
        # turning on only one pin
        self.running = True
        if pin_num == self.pin1_num:
            self.direction = 1
            # pin 2 input
            pin2 = machine.ADC(machine.Pin(self.pin2_num))
            pin2.atten(machine.ADC.ATTN_11DB)
            # on pin1
            pin1 = machine.Pin(self.pin1_num, machine.Pin.OUT)
            pin1.on()
        if pin_num == self.pin2_num:
            self.direction = 2
            # pin 1 input
            pin1 = machine.ADC(machine.Pin(self.pin1_num))
            pin1.atten(machine.ADC.ATTN_11DB)
            # on pin2
            pin2 = machine.Pin(self.pin2_num, machine.Pin.OUT)
            pin2.on()

    def on(self):
        """ starts motor in direction set """
        self.on_direction(self.direction)

    def on_direction(self, direct):
        """ starts motor in direction given """
        if direct == 1:
            self.on_pin(self.pin1_num)
        if direct == 2:
            self.on_pin(self.pin2_num)

    def off(self):
        """ stops motor """
        self.running = False
        pin1 = machine.Pin(self.pin1_num, machine.Pin.OUT)
        pin1.off()
        pin2 = machine.Pin(self.pin2_num, machine.Pin.OUT)
        pin2.off()

    def is_running(self):
        """ if the motor is running or not """
        return self.running

    def get_direction(self):
        """ the direction selected """
        return self.direction
