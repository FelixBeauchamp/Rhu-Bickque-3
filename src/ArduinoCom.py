import serial
import time

# To change if different port
com_port1 = 'COM3'

motor_state = 'openedX_openedY'
serial1 = serial.Serial(com_port1, 230400)
com_state = 'Closed'

def openport():

    global com_state
    global serial1

    serial1.close()
    serial1.open()

    com_state = 'Opened'

    end = 'finished open port 1'

    time.sleep(1)

    return end

def closeport():
    global com_state
    global serial1

    serial1.close()

    com_state1 = 'Closed'

    end = 'finished close port'

    return end

def sendmessage(megawhat):

    global motor_state

    # Send a string to Arduino
    message = megawhat
    serial1.write(message.encode())

    # Read the response from Arduino
    motor_state = serial1.readline().decode()

    # Print the response
    print("Response from Arduino:", motor_state)

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
openport()
start_time = time.time()
sendmessage('CXCY')
end_time = time.time()
closeport()
print(end_time - start_time)