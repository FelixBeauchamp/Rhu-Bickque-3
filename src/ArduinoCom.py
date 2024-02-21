import serial
import time

motor_stateArduino = 'openedX_openedY'
com_stateArduino = 'Closed'

def openportarduino(com_port1):

    global com_stateArduino
    global serialArduino

    serialArduino = serial.Serial(com_port1, 230400)

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

    # Send a string to Arduino
    message = megawhat
    serialArduino.write(message.encode())

    # Read the response from Arduino
    motor_stateArduino = serialArduino.readline().decode()

    # Print the response
    print("Response from Arduino:", motor_stateArduino)

    end = 'finished servo-motor spin'

    return end

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
