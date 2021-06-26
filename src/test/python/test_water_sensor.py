import unittest

from src.main.python.water_sensor import WaterSensor


class TestWaterSensor(unittest.TestCase):
    ws = WaterSensor(33)

    def test_create(self):
        ws2 = WaterSensor(34)
        self.assertEqual(self.ws.get_last_measure(), ws2.get_last_measure())

    def test_measure(self):
        self.assertEqual(self.ws.measure(), 0)
        self.assertEqual(self.ws.measure(), self.ws.get_last_measure())

    def test_otherFunctions(self):
        self.ws.measure()
        self.ws.get_percentage()
        self.ws.get_average()
        self.ws.get_liters()

    def test_printSensor(self):
        ws3 = WaterSensor(99, range_min=200, range_max=1000, average_converging_speed=1, capacity=2)
        ws3.measure()
        print(ws3)
        print(self.ws)


if __name__ == '__main__':
    unittest.main()
