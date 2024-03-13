import serial
import time
import struct

motor_stateArduino = 0
com_stateArduino = 'Closed'
serialArduino = serial.Serial('COM3', 57600)

def openportarduino():

    global com_stateArduino
    global serialArduino

    serialArduino.close()
    serialArduino.open()

    com_stateArduino = 'Opened'

    end = 'finished open port 1'

    time.sleep(1)

    return end

def closeportarduino():
    global com_stateArduino
    global serialArduino

    serialArduino.close()

    com_stateArduino = 'Closed'

    end = 'finished close port'

    return end

def sendmessage(megawhat):

    global motor_stateArduino
    global serialArduino

    info = 0

    if megawhat == 'OXOY':
        info = 1
    if megawhat == 'CXOY':
        info = 2
    if megawhat == 'OXCY':
        info = 3
    if megawhat == 'CXCY':
        info = 4

    # Send a string to Arduino
    message = struct.pack('<i', info)
    serialArduino.write(message)

    end = 'finished servo-motor spin'
    megadone()
    motor_stateArduino = 0
    return end

def readmessage():
    global serialArduino
    global motor_stateArduino

    """
    binary_data = serialArduino.read(4)  # Assuming you are expecting a 4-byte integer

    motor_stateArduino = int((struct.unpack('<i', binary_data)[0])/65537)
    """
    response = serialArduino.readline().decode().strip()

    if response == 'yo':
        motor_stateArduino = 1
    # Print the response
    print("Response from Arduino:", motor_stateArduino)

    return motor_stateArduino

def megadone():
    while True:
        if readmessage() == 1:
            time.sleep(0.5)
            break

"""
# format example for megawhat command: 'OXOY'
# format example for com_port: 'COM3'
def sendtomega(megawhat,com_port):

    # Global Variable
    global motor_state

    # Open the serial port (adjust the port and baud rate as needed)
    ser = serial.Serial(com_port, 9600)

    ser.close()
    ser.open()

    time.sleep(1)
    # Send a string to Arduino
    message = megawhat
    ser.write(message.encode())

    # Read the response from Arduino
    motor_state = ser.readline().decode()

    # Print the response
    print("Response from Arduino:", motor_state)

    # Close the serial port
    ser.close()

    end = 'finished servo-motor spin'

    return end
"""

openportarduino()
sendmessage('CXCY')
sendmessage('OXOY')
closeportarduino()
