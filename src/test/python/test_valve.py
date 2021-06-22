import unittest

from src.main.python.valve import Valve


class TestValve(unittest.TestCase):

    def test_create(self):
        self.valve = Valve(99)
        v2 = Valve(34)
        self.assertEqual(self.valve.status(), v2.status())

    def open_close(self):
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

    def switch(self):
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

    def status(self):
        v5 = Valve(99, initial_opened=True)
        self.assertEqual("opened", v5.status())
        v5.switch()
        self.assertEqual("closed", v5.status())
        v5.switch()
        self.assertEqual("opened", v5.status())

    def printSensor(self):
        print(self.valve)


if __name__ == '__main__':
    unittest.main()
