import unittest

from src.main.python.servo import Servo


class TestServo(unittest.TestCase):

    servo = Servo(99)

    def test_create(self):
        s2 = Servo(34)
        self.assertEqual(self.servo.get_angle(), s2.get_angle())

    def test_angle(self):
        s3 = Servo(3, range_min=30, range_max=130, frequency=50)
        self.assertEqual(self.servo.get_angle(), s3.get_angle())
        self.assertEqual(self.servo.get_angle(), 0)
        # move
        self.assertTrue(s3.angle(50))
        self.assertTrue(s3.angle(110))
        # out of range
        self.assertFalse(s3.angle(0))
        self.assertFalse(s3.angle(200))

    def test_printSensor(self):
        s4 = Servo(3, range_min=50, range_max=7, frequency=50)
        print(s4)
        print(self.servo)


if __name__ == '__main__':
    unittest.main()
