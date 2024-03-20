import unittest
import sys
import OpenRBCom
import time
port_OpenRB_test = 'COM8'


class TestComDynamixel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize any necessary resources before all test methods in the class
        # For example, open the port
        OpenRBCom.openport(port_OpenRB_test)
    @classmethod
    def tearDownClass(cls):
        # Clean up resources after all test methods in the class have been run
        # For example, close the port
        OpenRBCom.closeport()
    def test_homing(self):
        self.assertEqual(OpenRBCom.sendmessage('HOMING')
, 'Finished Dynamixel spin',
                         "Should put all the Dynamixel in their initial position and return value of 1")
    def test_M1_L(self):
        self.assertEqual(OpenRBCom.sendmessage('M1_L'), 'Finished Dynamixel spin',
                         "Motor 1 should to a 90 degree clockwise rotation")

    def test_M1_R(self):
        self.assertEqual(OpenRBCom.sendmessage("M1_R"), 'Finished Dynamixel spin',
                         "Motor 1 should to a 90 degree counter-clockwise rotation")
    def test_M2_L(self):
        self.assertEqual(OpenRBCom.sendmessage("M2_L"), 'Finished Dynamixel spin',
                         "Motor 2 should to a 90 degree clockwise rotation")

    def test_M2_R(self):
        self.assertEqual(OpenRBCom.sendmessage("M2_R"), 'Finished Dynamixel spin',
                         "Motor 2 should to a 90 degree counter-clockwise rotation")
    def test_M3_L(self):
        self.assertEqual(OpenRBCom.sendmessage("M3_L"), 'Finished Dynamixel spin',
                         "Motor 3 should to a 90 degree clockwise rotation")

    def test_M3_R(self):
        self.assertEqual(OpenRBCom.sendmessage("M3_R"), 'Finished Dynamixel spin',
                         "Motor 3 should to a 90 degree counter-clockwise rotation")
    def test_M4_L(self):
        self.assertEqual(OpenRBCom.sendmessage("M4_L"), 'Finished Dynamixel spin',
                         "Motor 4 should to a 90 degree clockwise rotation")

    def test_M4_R(self):
        self.assertEqual(OpenRBCom.sendmessage("M4_R"), 'Finished Dynamixel spin',
                         "Motor 4 should to a 90 degree counter-clockwise rotation")

    def test_M1M3_L(self):
        self.assertEqual(OpenRBCom.sendmessage("M1M3_L"), 'Finished Dynamixel spin',
                         "Motor 1 and Motor 3 should do a 90 clockwise rotation based on the first motor")

    def test_M1M3_R(self):
        self.assertEqual(OpenRBCom.sendmessage("M1M3_R"), 'Finished Dynamixel spin',
                         "Motor 1 and Motor 3 should do a 90 counter-clockwise rotation based on the first motor")

    def test_M2M4_L(self):
        self.assertEqual(OpenRBCom.sendmessage("M2M4_L"), 'Finished Dynamixel spin',
                         "Motor 2 and Motor 4 should do a 90 clockwise rotation based on the first motor")

    def test_M2M4_R(self):
        self.assertEqual(OpenRBCom.sendmessage("M2M4_R"), 'Finished Dynamixel spin',
                         "Motor 2 and Motor 4 should do a 90 counter-clockwise rotation based on the first motor")


if __name__ == '__main__':
    print("The test result cannot confirm if the Dynamixel motors actually did the right move. It only confirms that the communication protocol works.")
    #OpenRBCom.openport(port_OpenRB_test)
    unittest.main()
    #OpenRBCom.closeport()
