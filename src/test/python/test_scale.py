import unittest

from src.main.python.scale import Scale


class TestScaleSensor(unittest.TestCase):

    def test_create(self):
        self.scale = Scale(pin_sck=32, pin_out_dt=34)
        sc2 = Scale(88, 89)
        self.assertEqual(self.scale.get_last_measure(), sc2.get_last_measure())

    def measure(self):
        self.scale.measure()
        self.assertEqual(self.scale.measure(), self.scale.measure())
        self.assertEqual(self.scale.measure(), self.scale.get_last_measure())

    def otherFunctions(self):
        self.scale.raw_value()
        self.scale.tare()
        self.scale.measure()
        self.scale.get_mean()
        self.scale.percentage()

    def weight(self):
        self.scale.measure()
        self.assertEqual(self.scale.weight() * 1000, self.scale.weight_kg())

    def printSensor(self):
        sc3 = Scale(77, 66)
        sc3.measure()
        print(sc3)
        print(self.scale)


if __name__ == '__main__':
    unittest.main()
