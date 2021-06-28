import unittest

from src.main.python.valve import Valve


class TestValve(unittest.TestCase):
    valve = Valve(99)

    def test_create(self):
        v2 = Valve(34)
        self.assertEqual(self.valve.status(), v2.status())

    def test_open_close(self):
        v3 = Valve(88, initial_opened=True)
        self.assertTrue(v3.is_open())
        self.assertFalse(v3.is_closed())
        v4 = Valve(88, initial_opened=False)
        self.assertTrue(v4.is_closed())
        self.assertFalse(v4.is_open())
        # open
        v3.open()
        v4.open()
        self.assertTrue(v3.is_open())
        self.assertTrue(v4.is_open())
        self.assertFalse(v3.is_closed())
        self.assertFalse(v4.is_closed())
        # close
        v3.close()
        v4.close()
        self.assertTrue(v3.is_closed())
        self.assertTrue(v4.is_closed())
        self.assertFalse(v3.is_open())
        self.assertFalse(v4.is_open())

    def test_switch(self):
        v3 = Valve(88, initial_opened=True)  # switched below
        v4 = Valve(88, initial_opened=False)  # switched below
        # switch
        v3.switch()
        v4.switch()
        self.assertTrue(v3.is_closed())
        self.assertFalse(v3.is_open())
        self.assertTrue(v4.is_open())
        self.assertFalse(v4.is_closed())

        v3.switch()
        v4.switch()
        self.assertTrue(v3.is_open())
        self.assertFalse(v3.is_closed())
        self.assertTrue(v4.is_closed())
        self.assertFalse(v4.is_open())

        v3.switch()
        v4.switch()
        self.assertTrue(v3.is_closed())
        self.assertFalse(v3.is_open())
        self.assertTrue(v4.is_open())
        self.assertFalse(v4.is_closed())

    def test_status(self):
        v5 = Valve(99, initial_opened=True)
        self.assertEqual("opened", v5.status())
        v5.switch()
        self.assertEqual("closed", v5.status())
        v5.switch()
        self.assertEqual("opened", v5.status())

    def test_printSensor(self):
        v6 = Valve(45, initial_opened=True)
        v6.switch()
        print(v6)
        print(self.valve)


if __name__ == '__main__':
    unittest.main()
