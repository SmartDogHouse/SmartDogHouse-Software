import machine
from sensor import Sensor


class SensorADC(Sensor):
    """Sensor, measures an amount from a pin with ADC """

    def __init__(self, pin_num, range_min=0, range_max=4000, average_converging_speed=1 / 2):
        """ constructor.
        :param pin_num: number pin that will read value, it has to be ADC, analog to digital converter
        :param range_min: min value of sensor
        :param range_max: max value of sensor
        :param average_converging_speed: speed the average goes towards the last measure (range 0-1) """
        super().__init__(range_min, range_max, average_converging_speed)
        self.pin = machine.ADC(machine.Pin(pin_num))
        self.pin.atten(machine.ADC.ATTN_6DB)  # increase reading voltage to 2V

    def measure(self):
        """ measures, updates average, returns raw measure """
        return super().measure(self.pin.read())

