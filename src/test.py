# This files contains the majority of unitary / small integration tests. They majoritarily revolve around communication protocol.

import unittest
import sys
import OpenRBCom
import ArduinoCom
import traitement_image


# The ports to be used and the expected colors results form the face of the cube to analyze must be decided before running tests
port_Arduino_test = 'COM9'
port_OpenRB_test = 'COM8'
expected_result_faceofthecube = ['B', 'B', 'B', 'R', 'R', 'R', 'O', 'O', 'O']

OpenRB_EndCom_Message = 'Finished Dynamixel spin'
Arduino_EndCom_Message = 'Finished ServoMotor movement'

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
        self.assertEqual(OpenRBCom.sendmessage('HOMING'), OpenRB_EndCom_Message,
                         "Should put all the Dynamixel in their initial position and return value of 1")
    def test_M1_L(self):
        self.assertEqual(OpenRBCom.sendmessage('M1_L'), OpenRB_EndCom_Message,
                         "Motor 1 should to a 90 degree clockwise rotation")
    def test_M1_R(self):
        self.assertEqual(OpenRBCom.sendmessage("M1_R"), OpenRB_EndCom_Message,
                         "Motor 1 should to a 90 degree counter-clockwise rotation")
    def test_M2_L(self):
        self.assertEqual(OpenRBCom.sendmessage("M2_L"), OpenRB_EndCom_Message,
                         "Motor 2 should to a 90 degree clockwise rotation")
    def test_M2_R(self):
        self.assertEqual(OpenRBCom.sendmessage("M2_R"), OpenRB_EndCom_Message,
                         "Motor 2 should to a 90 degree counter-clockwise rotation")
    def test_M3_L(self):
        self.assertEqual(OpenRBCom.sendmessage("M3_L"), OpenRB_EndCom_Message,
                         "Motor 3 should to a 90 degree clockwise rotation")
    def test_M3_R(self):
        self.assertEqual(OpenRBCom.sendmessage("M3_R"), OpenRB_EndCom_Message,
                         "Motor 3 should to a 90 degree counter-clockwise rotation")
    def test_M4_L(self):
        self.assertEqual(OpenRBCom.sendmessage("M4_L"), OpenRB_EndCom_Message,
                         "Motor 4 should to a 90 degree clockwise rotation")
    def test_M4_R(self):
        self.assertEqual(OpenRBCom.sendmessage("M4_R"), OpenRB_EndCom_Message,
                         "Motor 4 should to a 90 degree counter-clockwise rotation")
    def test_M1M3_L(self):
        self.assertEqual(OpenRBCom.sendmessage("M1M3_L"), OpenRB_EndCom_Message,
                         "Motor 1 and Motor 3 should do a 90 clockwise rotation based on the first motor")
    def test_M1M3_R(self):
        self.assertEqual(OpenRBCom.sendmessage("M1M3_R"), OpenRB_EndCom_Message,
                         "Motor 1 and Motor 3 should do a 90 counter-clockwise rotation based on the first motor")
    def test_M2M4_L(self):
        self.assertEqual(OpenRBCom.sendmessage("M2M4_L"), OpenRB_EndCom_Message,
                         "Motor 2 and Motor 4 should do a 90 clockwise rotation based on the first motor")
    def test_M2M4_R(self):
        self.assertEqual(OpenRBCom.sendmessage("M2M4_R"), OpenRB_EndCom_Message,
                         "Motor 2 and Motor 4 should do a 90 counter-clockwise rotation based on the first motor")


class TestComServoMotor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize any necessary resources before all test methods in the class
        # For example, open the port
        ArduinoCom.openportarduino(port_Arduino_test)
    @classmethod
    def tearDownClass(cls):
        # Clean up resources after all test methods in the class have been run
        # For example, close the port
        ArduinoCom.closeportarduino()
    def test_homing(self):
        self.assertEqual(ArduinoCom.sendmessage('OXOY'), Arduino_EndCom_Message,
                     "Should put the two ServoMotor in their homing position. The Dynamixel motors should be all spaced")

    def test_Xclose_Yopen(self):
        self.assertEqual(ArduinoCom.sendmessage('CXOY'), Arduino_EndCom_Message,
                         "Should put the ServoMotor in the X axis closed and Y axis opened. The Dynamixel motors on X axis close to center and Dynamixel motors in Y axis away from center")
    def test_Xopen_Yclose(self):
        self.assertEqual(ArduinoCom.sendmessage('OXCY'), Arduino_EndCom_Message,
                         "Should put the ServoMotor in the X axis opened and Y axis closed. The Dynamixel motors on X axis away from center and Dynamixel motors in Y axis near the center")
    def test_allclosed(self):
        self.assertEqual(ArduinoCom.sendmessage('CXCY'), Arduino_EndCom_Message,
                         "Should put the two ServoMotor in their closed position. The Dynamixel motors should all be near the center")

class TestTraitementImage(unittest.TestCase):
    '''def setUp(self):
        # Prompt the user to input expected results
        print("Please enter the expected results for the face of the cube (comma-separated):")
        expected_input = input().strip().split(',')
        # Convert input to list of strings
        self.expected_result = [x.strip() for x in expected_input]'''
    def test_faceofdacube(self):
        # Call the function
        results = traitement_image.faceofdacube()
        # Compare the actual result with the expected result
        self.assertEqual(results, expected_result_faceofthecube, f"Expected: {expected_result_faceofthecube}, Got: {results}")


if __name__ == '__main__':

    # To run all the tests
    print("The tests results from motors cannot confirm if the Dynamixel motors ans ServoMotors actually did the right move. It only confirms that the communication protocol works.")
    unittest.main()
