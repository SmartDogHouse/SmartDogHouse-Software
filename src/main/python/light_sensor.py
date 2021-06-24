import machine


class LightSensor:
    """LightSensor, measures amount of light """

    last_measure = -1

    def __init__(self, pin_num, range_min=0, range_max=4000, mean_converge_speed=1/2, threshold=3000):
        """ constructor.
        :param pin_num: number pin that will read value, it has to be ADC, analog to digital converter
        :param range_min: min value of sensor (empty),
        :param range_max: max value of sensor (full),
        :param threshold: limit below is light, above it's dark  """
        self.pin = machine.ADC(machine.Pin(pin_num))
        self.pin.atten(machine.ADC.ATTN_6DB)  # increase reading voltage to 2V
        self.range_min = range_min
        self.range_max = range_max
        self.mean_converge_speed = mean_converge_speed
        self.mean = (range_min + range_max) / 2
        self.threshold = threshold

    def __str__(self):
        """ prints the object """
        return "LightSensor: mean: {}, last measure {}, perc: {}, threshold: {}".format(self.mean, self.last_measure,
                                                                                        self.get_percentage(),
                                                                                        self.threshold)

    def measure(self):
        """ measures sensor  (0 is lighter) """
        self.last_measure = self.pin.read()
        self.mean = self.last_measure * self.mean_converge_speed + self.mean * (1 - self.mean_converge_speed)
        return self.last_measure

    def get_last_measure(self):
        """ last measure, not to use directly, better get_mean() """
        return self.last_measure

    def get_mean(self):
        """ mean recent measures, more constant than last measure  """
        return self.mean

    def get_percentage(self):
        """ actual percentage of light (0 is lighter)  """
        return (self.mean - self.range_min) / (self.range_max - self.range_min)

    def is_light(self):
        """ true if below threshold of light  """
        return self.mean < self.threshold

    def is_dark(self):
        """ true if above threshold  """
        return not self.is_light()

