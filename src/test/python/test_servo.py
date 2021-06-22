import unittest

from src.main.python.servo import Servo


class TestServo(unittest.TestCase):

    def test_create(self):
        self.servo = Servo(99)
        s2 = Servo(34)
        self.assertEqual(self.servo.get_angle(), s2.get_angle())

    def angle(self):
        s3 = Servo(3, range_min=30, range_max=130, frequency=50)
        self.assertEqual(self.servo.get_angle(), s3.get_angle())
        self.assertTrue(self.servo.get_angle())
        # move
        self.assertTrue(s3.angle(50))
        self.assertTrue(s3.angle(110))
        # out of range
        self.assertFalse(s3.angle(0))
        self.assertFalse(s3.angle(200))

    def printSensor(self):
        print(self.servo)


if __name__ == '__main__':
    unittest.main()
