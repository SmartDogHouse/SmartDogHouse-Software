import unittest

from src.main.python.water_sensor import WaterSensor


class TestWaterSensor(unittest.TestCase):

    def test_create(self):
        self.ws = WaterSensor(33)
        ws2 = WaterSensor(34)
        self.assertEqual(self.ws.get_last_measure(), ws2.get_last_measure())

    def measure(self):
        self.assertEqual(self.ws.measure(), 0)
        self.assertEqual(self.ws.measure(), self.ws.get_last_measure())

    def otherFunctions(self):
        self.ws.measure()
        self.ws.get_percentage()
        self.ws.get_mean()
        self.ws.get_liters()

    def printSensor(self):
        ws3 = WaterSensor()
        ws3.measure()
        print(ws3)


if __name__ == '__main__':
    unittest.main()
