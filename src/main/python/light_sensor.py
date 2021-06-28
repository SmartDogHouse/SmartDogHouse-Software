import machine
from sensor_adc import SensorADC


class LightSensor(SensorADC):

    """LightSensor, measures amount of light"""

    def __init__(self, pin_num, range_min=0, range_max=4000, average_converging_speed=1 / 2, threshold=3000):
        """constructor.
        :param pin_num: number pin that will read value, it has to be ADC, analog to digital converter
        :param range_min: min value of sensor (empty),
        :param range_max: max value of sensor (full),
        :param threshold: limit below is light, above it's dark  """
        super().__init__(pin_num, range_min, range_max, average_converging_speed)
        self.threshold = threshold

    def __str__(self):
        """prints the object"""
        return "LightSensor: average: {}, last measure {}, percentage: {}, threshold: {}".format(self.get_average(),
                                                                                                 self.last_measure,
                                                                                                 self.get_percentage(),
                                                                                                 self.threshold)

    def measure(self):
        """measures sensor  (0 is lighter)"""
        return super().measure()

    def get_percentage(self):
        """actual percentage of light (0 is lighter)"""
        return super().get_percentage()

    def is_light(self):
        """true if below threshold of light"""
        return self.get_average() < self.threshold

    def is_dark(self):
        """true if above threshold"""
        return not self.is_light()
