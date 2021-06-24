import unittest

from src.main.python.motor import Motor


class TestMotor(unittest.TestCase):

    def test_create(self):
        self.motor = Motor(99)
        m2 = Motor(88)
        self.assertEqual(self.motor.is_running(), m2.is_running())
        m3 = Motor(77,running=True)
        self.assertTrue(m3.is_running())
        m3 = Motor(77,running=False)
        self.assertFalse(m3.is_running())

    def start(self):
        self.motor.on()
        self.assertTrue(self.motor.is_running())
        self.motor.off()
        self.assertFalse(self.motor.is_running())
        self.motor.on()
        self.assertTrue(self.motor.is_running())


    def print(self):
        m3 = Motor(66)
        m3.on()
        m3.off()
        print(m3)
        print(self.motor)


if __name__ == '__main__':
    unittest.main()
