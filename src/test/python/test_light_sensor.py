import unittest

from src.main.python.light_sensor import LightSensor


class TestLightSensor(unittest.TestCase):
    ls = LightSensor(33)

    def test_create(self):
        ls2 = LightSensor(34)
        self.assertEqual(self.ls.get_last_measure(), ls2.get_last_measure())

    def test_measure(self):
        self.assertEqual(self.ls.measure(), 0)
        self.assertEqual(self.ls.measure(), self.ls.get_last_measure())

    def test_otherFunctions(self):
        self.ls.measure()
        self.ls.get_percentage()
        self.ls.get_mean()
        self.assertEqual(self.ls.is_light(), not self.ls.is_dark())

    def test_printSensor(self):
        ls3 = LightSensor(99, range_min=100, range_max=3000, mean_converge_speed=1/9, threshold=2500)
        ls3.measure()
        print(ls3)
        print(self.ls)


if __name__ == '__main__':
    unittest.main()
