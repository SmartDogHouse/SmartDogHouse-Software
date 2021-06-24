import unittest

from src.main.python.motor_bidirectional import MotorBidirectional


class TestMotorBidirectional(unittest.TestCase):
    motor = MotorBidirectional(88, 99)

    def test_create(self):
        m2 = MotorBidirectional(88, 99)
        self.assertEqual(self.motor.is_running(), m2.is_running())
        m3 = MotorBidirectional(77, 88, running=True)
        self.assertTrue(m3.is_running())
        m3 = MotorBidirectional(77, 88, running=False)
        self.assertFalse(m3.is_running())

    def test_start(self):
        self.motor.on()
        self.assertTrue(self.motor.is_running())
        self.motor.off()
        self.assertFalse(self.motor.is_running())
        self.motor.on()
        self.assertTrue(self.motor.is_running())

    def test_direction(self):
        m5 = MotorBidirectional(66, 88, running=True, direction=1)
        self.assertEqual(1, m5.get_direction())
        m5.on_direction(1)
        self.assertTrue(m5.running)
        self.assertEqual(1, m5.get_direction())
        m5.on_direction(2)
        self.assertTrue(m5.running)
        m5.off()
        self.assertFalse(m5.is_running())
        self.assertEqual(2, m5.get_direction())
        m5.on_direction(1)
        self.assertTrue(m5.running)
        self.assertEqual(1, m5.get_direction())

    def test_pin_direction(self):
        m6 = MotorBidirectional(pin1_num=66, pin2_num=88, running=True, direction=2)
        self.assertEqual(2, m6.get_direction())
        m6.on_pin(66)
        self.assertTrue(m6.running)
        self.assertEqual(1, m6.get_direction())
        m6.on_pin(88)
        self.assertTrue(m6.running)
        self.assertEqual(2, m6.get_direction())
        m6.off()
        self.assertFalse(m6.is_running())
        self.assertEqual(2, m6.get_direction())
        m6.on_pin(88)
        self.assertTrue(m6.running)
        self.assertEqual(2, m6.get_direction())

    def test_print(self):
        m3 = MotorBidirectional(66, 88, running=True, direction=2)
        m3.on()
        m3.off()
        print(m3)
        print(self.motor)


if __name__ == '__main__':
    unittest.main()
