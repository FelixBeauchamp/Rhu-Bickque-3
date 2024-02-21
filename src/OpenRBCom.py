import serial
import time

# To change if different port
com_port = 'COM7'

serial2 = serial.Serial(com_port, 57600)

com_state2 = 'Closed'

def openport():

    global com_state2
    global serial2

    serial2.close()
    serial2.open()

    com_state2 = 'Opened'

    end = 'finished open port 2'

    return end

def closeport():
    global com_state2
    global serial2

    serial2.close()

    com_state2 = 'Closed'

    end = 'finished close port 2'

    return end

def sendmessage(megawhat):

    time.sleep(1)
    # Send a string to Arduino
    message = megawhat
    serial2.write(message.encode())

    # Read the response from Arduino
    motor_state = serial2.readline().decode()

    end = 'finished servo-motor spin'

    return end

"""
# format example for megawhat command: 'OXOY'
# format example for com_port: 'COM3'
def sendtoRB(megawhat,com_port):

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

    end = 'finished dynamixel spin'

    return end
"""

