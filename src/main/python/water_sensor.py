import machine


# some modules, like "statistics" are not present in micropython


class WaterSensor:
    """WaterSensor, measures amount of water in a bowl """

    last_measure = -1

    def __init__(self, pin_num, range_min=0, range_max=2000, mean_converge_speed=1 / 2, max_liters=0.5):
        """ constuctor.
        :param pin_num: number pin of sensor,
        :param range_min: min value of sensor (empty ),
        :param range_max: max value of sensor (full ),
        :param max_liters: liters contained in the bowl full  """
        self.pin = machine.ADC(machine.Pin(pin_num))
        self.pin.atten(machine.ADC.ATTN_6DB)  # increase reading voltage to 2V
        self.range_min = range_min
        self.range_max = range_max
        self.mean_converge_speed = mean_converge_speed
        self.max_liters = max_liters
        self.mean = (range_min + range_max) / 2

    def __str__(self):
        """ prints the object """
        return "WaterSensor: mean: {}, last measure {}, perc: {}, liters: {}".format(self.mean, self.last_measure,
                                                                                     self.get_percentage(),
                                                                                     self.get_liters())

    def measure(self):
        """ measures sensor  """
        self.last_measure = self.pin.read()
        self.mean = self.last_measure * self.mean_converge_speed + self.mean * (1 - self.mean_converge_speed)
        return self.last_measure

    def get_last_measure(self):
        """ last measure, not to use directly, better get_mean() """
        return self.last_measure

    def get_mean(self):
        """ mean of water in the bowl, more constant than last measure  """
        return self.mean

    def get_percentage(self):
        """ actual percentage of water in the bowl  """
        return (self.mean - self.range_min) / (self.range_max - self.range_min)

    def get_liters(self):
        """ actual liters in the bowl  """
        return self.get_percentage() * self.max_liters
