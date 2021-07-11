from sensor_adc import SensorADC


class PulseSensor(SensorADC):
    """PulseSensor, measures amount pressure in the blood"""

    def __init__(self, pin_num, range_min=0, range_max=4000, average_converging_speed=1 / 2):
        """ constructor.
        :param pin_num: number pin that will read value, it has to be ADC, analog to digital converter
        :param range_min: min value of sensor ,
        :param range_max: max value of sensor ,
        :param average_converging_speed: speed the average goes towards the last measure (range 0-1)
        """
        super().__init__(pin_num, range_min, range_max, average_converging_speed, attenuation=11)

    def __str__(self):
        """prints the object."""
        return "PulseSensor: average: {}, last measure {}, percentage: {}".format(self.get_average(),
                                                                                  self.get_last_measure(),
                                                                                  self.get_percentage()
                                                                                  )
