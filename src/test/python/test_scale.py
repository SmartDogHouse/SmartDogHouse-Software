import unittest

from src.main.python.scale import Scale


class TestScaleSensor(unittest.TestCase):
    scale = Scale(pin_sck=32, pin_out_dt=34)

    def test_create(self):
        sc2 = Scale(88, 89)
        self.assertEqual(self.scale.get_last_measure(), sc2.get_last_measure())

    def test_measure(self):
        self.scale.raw_measure()
        self.assertEqual(self.scale.raw_measure(), self.scale.raw_measure())
        self.scale.measure()
        self.assertEqual(self.scale.measure(), self.scale.get_last_measure())

    def test_otherFunctions(self):
        self.scale.raw_value()
        self.scale.tare()
        self.scale.raw_measure()
        self.scale.get_average()
        self.scale.get_percentage()

    def test_weight(self):
        self.scale.raw_measure()
        self.scale.measure()
        self.assertEqual(self.scale.weight() * 1000, self.scale.weight_kg())

    def test_printSensor(self):
        sc3 = Scale(77, 66, range_min=100, range_max=9000, average_converging_speed=1 / 6,
                    val_to_g_conversion=1000)
        sc3.raw_measure()
        print(sc3)
        print(self.scale)


if __name__ == '__main__':
    unittest.main()
