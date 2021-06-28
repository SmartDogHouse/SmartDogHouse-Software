from sensor_adc import SensorADC


class WaterSensor(SensorADC):

    """WaterSensor, measures amount of water in a bowl"""

    def __init__(self, pin_num, range_min=0, range_max=4000, average_converging_speed=1 / 2, capacity=0.5):

        """ constructor.
        :param pin_num: number pin that will read value, it has to be ADC, analog to digital converter
        :param range_min: min value of sensor (empty),
        :param range_max: max value of sensor (full),
        :param average_converging_speed: speed the average goes towards the last measure (range 0-1)
        :param capacity: liters contained in the bowl full  """
        super().__init__(pin_num, range_min, range_max, average_converging_speed)
        self.capacity = capacity

    def __str__(self):
        """prints the object."""
        return "WaterSensor: average: {}, last measure {}, percentage: {}, liters: {}".format(self.get_average(),
                                                                                              self.get_last_measure(),
                                                                                              self.get_percentage(),
                                                                                              self.get_liters())

    def get_percentage(self):
        """actual percentage of water in the bowl."""
        return super().get_percentage()

    def get_liters(self):
        """actual liters in the bowl."""
        return self.get_percentage() * self.capacity
