import serial
import time

state = 'openedX_openedY'

# megawhat format example: 'OXOY'
# com_port format example: 'COM3'
def sendtomega(megawhat,com_port):

    # Global Variable
    global state

    # Open the serial port (adjust the port and baud rate as needed)
    ser = serial.Serial(com_port, 9600)

    ser.close()
    ser.open()

    time.sleep(1)
    # Send a string to Arduino
    message = megawhat
    ser.write(message.encode())

    # Wait for a short time to ensure Arduino has processed the input
    time.sleep(1)

    # Read the response from Arduino
    state = ser.readline().decode()

    # Print the response
    print("Response from Arduino:", state)

    # Close the serial port
    ser.close()

    end = 'finished'

    return end

