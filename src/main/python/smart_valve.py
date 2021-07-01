import machine
from src.main.python.sensor import Sensor
from valve import Valve
from water_sensor import WaterSensor


class SmartValve:

    def __init__(self, valve_pin: int, water_pin: int, min_lvl: int, max_lvl: int):
        """ constructor.
        """
        self.minLvl = min_lvl
        self.maxLvl = max_lvl
        self.valve = Valve(valve_pin)
        self.waterSensor = WaterSensor(water_pin)

    def __str__(self):
        """prints the object."""
        return "Motor bidirectional currently is running: {}, direction: {}"

    async def __getBehaviour(self):
        self.waterSensor.measure()
        if self.waterSensor.get_average() < self.minLvl:
            self.valve.open()
            while self.waterSensor.get_average() < self.maxLvl:
                self.waterSensor.measure()
            self.valve.close()

    def behaviour(self):
        return self.__getBehaviour

    def setMaxWaterLevel(self, max_lvl):
        self.maxLvl = max_lvl

    def setMinWaterLevel(self, min_lvl):
        self.minLvl = min_lvl
