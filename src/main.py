import UI
import control
import sys

# These ports can be found with ArduinoIDE
port_Arduino = 'COM7'  # Select the right port to the Arduino from your computer.
port_OpenRB = 'COM6'  # Select the right port to the OpenRb from your computer

cam_number = 0  # Select the right number of the port from your computer for the Camera. Usually between 0 and 2

if __name__ == '__main__':
    # Initialize face colors to all white
    control.port_Arduino = port_Arduino
    control.port_OpenRB = port_OpenRB
    control.cam_number_control = cam_number
    initial_face_colors = {
        "Back": ['red'] * 9,
        "Left": ['green'] * 9,
        "Top": ['yellow'] * 9,
        "Right": ['blue'] * 9,
        "Front": ['orange'] * 9,
        "Bottom": ['white'] * 9
    }

    app = UI.QApplication(sys.argv)
    cube_display = UI.CubeDisplay(initial_face_colors)
    cube_display.show()

    sys.exit(app.exec_())
