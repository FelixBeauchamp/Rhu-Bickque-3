import unittest
import sys
import OpenRBCom
import time
port_OpenRB = 'COM8'


class TestDynamixel(unittest.TestCase):
    #def setUp(self):
        # Initialize any necessary resources before each test method is called
     #   OpenRBCom.openport(port_OpenRB)
    def test_What_the_flip(self):
        self.assertEqual(1, 1,
                         "Should put all the Dynamixel in their initial position and return value of 1")
    def test_homing(self):
        OpenRBCom.openport(port_OpenRB)
        self.assertEqual(OpenRBCom.sendmessage("HOMING"), 1,
                         "Should put all the Dynamixel in their initial position and return value of 1")


if __name__ == '__main__':
    unittest.main()
    OpenRBCom.closeport()
