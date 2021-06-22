import machine
from hx711 import HX711


class Scale:
    """Scale, measures a weight """

    last_measure = -1
    offset = 0

    def __init__(self, pin_sck, pin_out_dt, range_min=0, range_max=1000000, mean_converge_speed=1 / 2,
                 val_to_g_conversion=1220):
        """ constructor.
        :param pin_sck: number pin Serial Clock Input. it has to be output, es pin32 on ESP32
        :param pin_out_dt: number pin that will read data value, is has to be GPIO
        :param range_min: min value of sensor (empty), used for percentage
        :param range_max: max value of sensor (full), used for percentage
        :param val_to_g_conversion: to convert signal to grams (signal/val = g)"""
        machine.freq(160000000)
        self.driver = HX711(d_out=pin_out_dt, pd_sck=pin_sck)
        # self.driver.channel = HX711.CHANNEL_A_64
        self.range_min = range_min
        self.range_max = range_max
        self.mean = (range_min + range_max) / 2
        self.mean_converge_speed = mean_converge_speed
        self.val_to_g_conversion = val_to_g_conversion

    def __str__(self):
        """ prints the object """
        return "Scale: mean: {}, measure {}, perc: {}, weight: {}".format(self.mean,
                                                                          self.measure(),
                                                                          self.percentage(),
                                                                          self.weight())

    def raw_value(self):
        """ measures sensor, returns raw value"""
        return self.driver.read()

    def tare(self):
        """ tares sensor at empty scale"""
        self.offset = self.driver.read()

    def measure(self):
        """ returns sensor measure with tare (raw value - offset)"""
        self.last_measure = self.driver.read() - self.offset
        self.mean = self.last_measure * self.mean_converge_speed + self.mean * (1 - self.mean_converge_speed)
        return self.last_measure

    def get_last_measure(self):
        """ last measure, raw data, get_mean() instead returns a weighted average with the previous ones """
        return self.last_measure

    def get_mean(self):
        """ mean of last measures, more constant than last measure  """
        return self.mean

    def percentage(self):
        """ actual percentage in the range passed  """
        self.measure()
        return (self.mean - self.range_min) / (self.range_max - self.range_min)

    def weight(self):
        """ actual weight in grams """
        self.measure()
        return self.get_last_measure() / self.val_to_g_conversion

    def weight_kg(self):
        """ actual weight in kilograms """
        return self.weight() / 1000
