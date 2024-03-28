import serial
import time
import struct

com_stateRB = 'Closed'
motor_stateRB = 0

def openport(port):

    global com_stateRB
    global serialRB

    serialRB = serial.Serial(port, 57600)

    serialRB.close()
    serialRB.open()

    com_stateRB = 'Opened'

    end = 'finished open port 2'
    time.sleep(1)
    return end

def closeport():
    global com_stateRB
    global serialRB

    serialRB.close()

    com_stateRB = 'Closed'

    end = 'finished close port 2'

    return end

def sendmessage(megawhat):
    global serialRB
    global motor_stateRB

    #time.sleep(1)
    # Send a string to Arduino

    info = 0

    if megawhat == 'HOMING':
        info = 0
    if megawhat == 'M1_L':
        info = 1
    if megawhat == 'M1_R':
        info = 2
    if megawhat == 'M2_L':
        info = 3
    if megawhat == 'M2_R':
        info = 4
    if megawhat == 'M3_L':
        info = 5
    if megawhat == 'M3_R':
        info = 6
    if megawhat == 'M4_L':
        info = 7
    if megawhat == 'M4_R':
        info = 8
    if megawhat == 'M1M3_L':
        info = 9
    if megawhat == 'M1M3_R':
        info = 10
    if megawhat == 'M2M4_L':
        info = 11
    if megawhat == 'M2M4_R':
        info = 12

    message = struct.pack('<i', info)
    serialRB.write(message)

    end = dynamixeldone()
    motor_stateRB = 0
    return end

def readmessage():
    global serialRB
    global motor_stateRB

    binary_data = serialRB.read(4)  # Assuming you are expecting a 4-byte integer
    motor_stateRB = int((struct.unpack('<i', binary_data)[0]))

    # Print the response

    return motor_stateRB

def dynamixeldone():

    while True:
        if readmessage() == 1:
            return 'Finished Dynamixel spin'
        if readmessage() == 2:
            return 'Error in Dynamixel spin'

"""
openport()
sendmessage('HOMING')
sendmessage('M1_L')
sendmessage('M2_R')
sendmessage('HOMING')
closeport()
"""


