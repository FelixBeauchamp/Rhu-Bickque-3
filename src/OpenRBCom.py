import serial
import time

com_stateRB = 'Closed'
motor_stateRB = "initialized"
def openport(com_port):

    global com_stateRB
    global serialRB

    serialRB = serial.Serial(com_port, 57600)

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

    global motor_stateRB

    #time.sleep(1)
    # Send a string to Arduino
    message = megawhat
    serialRB.write(message.encode())

    # Read the response from Arduino
    motor_stateRB = serialRB.readline().decode()

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

openport("COM8")
startime = time.time()
sendmessage("HOMING")
endtime = time.time()
sendmessage("M1M3_L")


sendmessage("M1_L")

closeport()
print(motor_stateRB)
print(endtime-startime)

