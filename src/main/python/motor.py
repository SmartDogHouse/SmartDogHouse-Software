import machine


class Motor:
    """Motor DC rotates in one direction with current """

    def __init__(self, pin_num, running=False):
        """ constructor.
        :param pin_num: number of pin that will give power to the motor
        """
        self.pin = machine.Pin(pin_num, machine.Pin.OUT)
        self.running = running
        self.pin.value(running)  # 1 to run, 0 to stop

    def __str__(self):
        """ prints the object """
        return "Motor currently is running: {}".format(self.running)

    def on(self):
        """ starts motor  """
        self.pin.on()
        self.running = True

    def off(self):
        """ stops motor  """
        self.pin.off()
        self.running = False

    def is_running(self):
        """ if the motor is running or not """
        return self.running
