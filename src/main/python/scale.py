import machine
from hx711 import HX711
from sensor import Sensor


class Scale(Sensor):
    """Scale, measures a weight """

    offset = 0

    def __init__(self, pin_sck, pin_out_dt, range_min=0, range_max=1000000, average_converging_speed=1 / 2,
                 val_to_g_conversion=1220):
        """ constructor.
        :param pin_sck: number pin Serial Clock Input. it has to be output, es pin32 on ESP32
        :param pin_out_dt: number pin that will read data value, is has to be GPIO
        :param range_min: min value of sensor (empty), used for percentage
        :param range_max: max value of sensor (full), used for percentage
        :param val_to_g_conversion: to convert signal to grams (signal/val = g)"""
        super().__init__(range_min, range_max, average_converging_speed)
        machine.freq(160000000)
        self.driver = HX711(d_out=pin_out_dt, pd_sck=pin_sck)
        # self.driver.channel = HX711.CHANNEL_A_64
        self.val_to_g_conversion = val_to_g_conversion

    def __str__(self):
        """ prints the object """
        return "Scale: average: {}, last measure {}, percentage: {}, weight: {}".format(self.get_average(),
                                                                                        self.get_last_measure(),
                                                                                        self.get_percentage(),
                                                                                        self.weight())

    def raw_value(self):
        """ measures sensor, returns raw value, not tared"""
        return self.driver.read()

    def tare(self):
        """ tares sensor at empty scale"""
        self.offset = self.driver.read()

    def measure(self):
        """ returns sensor measure with tare (raw value - offset)"""
        return super().measure( self.driver.read() - self.offset )

    def weight(self):
        """ actual weight in grams """
        self.measure()
        return self.get_last_measure() / self.val_to_g_conversion

    def weight_kg(self):
        """ actual weight in kilograms """
        return self.weight() / 1000
