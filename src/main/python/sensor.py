class Sensor:
    """Sensor, measures an amount """

    last_measure = -1

    def __init__(self, range_min=0, range_max=4095, average_converging_speed=1 / 2):
        """ constructor.
        :param range_min: min value of sensor
        :param range_max: max value of sensor
        :param average_converging_speed: speed the average goes towards the last measure (range 0-1) """
        self.range_min = range_min
        self.range_max = range_max
        self.average_converging_speed = average_converging_speed
        self.average = (range_min + range_max) / 2

    def __str__(self):
        """ prints the object """
        return "Sensor: average: {}, last measure {}, percentage: {}".format(self.get_average(),
                                                                             self.get_last_measure(),
                                                                             self.get_percentage())

    def measure(self, last_measure):
        """ measures, updates average, returns raw measure """
        self.last_measure = last_measure
        self.average = self.last_measure * self.average_converging_speed + self.average * (1-self.average_converging_speed)
        return self.last_measure

    def get_average(self):
        """ average (weighted exponentially) based on recent measures, more constant than last measure  """
        return self.average

    def get_last_measure(self):
        """ last measure, raw data, average() instead returns a weighted average with the previous ones """
        return self.last_measure

    def get_percentage(self):
        """ actual percentage of the average between range passed  """
        return (self.average - self.range_min) / (self.range_max - self.range_min)
