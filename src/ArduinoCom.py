import serial
import time
import struct

motor_stateArduino = 0
com_stateArduino = 'Closed'

def openportarduino(port):

    global com_stateArduino
    global serialArduino

    serialArduino = serial.Serial(port, 57600)

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
        info = 3
    if megawhat == 'OXCY':
        info = 2
    if megawhat == 'CXCY':
        info = 4

    # Send a string to Arduino
    message = struct.pack('<i', info)
    serialArduino.write(message)

    end = megadone()

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

    return motor_stateArduino

def megadone():
    while True:
        if readmessage() == 1:
            time.sleep(0.5)
            return 'Finished ServoMotor movement'

