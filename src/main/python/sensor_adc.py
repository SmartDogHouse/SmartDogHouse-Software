import machine
from sensor import Sensor


class SensorADC(Sensor):

    """Sensor, measures an amount from a pin with ADC """

    def __init__(self, pin_num, range_min=0, range_max=4000, average_converging_speed=1 / 2, attenuation=6):

        """ constructor.
        :param pin_num: number pin that will read value, it has to be ADC, analog to digital converter
        :param range_min: min value of sensor
        :param range_max: max value of sensor
        :param average_converging_speed: speed the average goes towards the last measure (range 0-1) """
        super().__init__(range_min, range_max, average_converging_speed)
        self.pin = machine.ADC(machine.Pin(pin_num))
        if attenuation == 0:
            self.pin.atten(machine.ADC.ATTN_0DB)   # maximum input voltage of 1.00v
        if attenuation == 2.5:
            self.pin.atten(machine.ADC.ATTN_2_5DB)  # maximum input voltage of 1.34V
        if attenuation == 6:
            self.pin.atten(machine.ADC.ATTN_6DB)  # increase reading voltage to 2V
        if attenuation == 11:
            self.pin.atten(machine.ADC.ATTN_11DB)  # maximum input voltage of 3.6V, going near this boundary may be damaging to the IC!

    def raw_measure(self):
        """measures, updates average, returns raw measure."""
        return self.pin.read()

