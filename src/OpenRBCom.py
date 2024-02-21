import serial
import time

def sendtoRB(megawhat):

    # Global Variable
    global state

    # Open the serial port (adjust the port and baud rate as needed)
    ser = serial.Serial('COM4', 9600)

    ser.close()
    ser.open()

    time.sleep(1)
    # Send a string to Arduino
    message = megawhat
    ser.write(message.encode())

    # Wait for a short time to ensure Arduino has processed the input
    time.sleep(1)

    # Read the response from Arduino
    response = ser.readline().decode()

    # Print the response
    print("Response from RB:", response)

    # Close the serial port
    ser.close()

    end = 'finished'

    return end

sendtoRB('M1_R')


