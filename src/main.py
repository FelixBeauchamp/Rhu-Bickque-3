import UI
import sys

if __name__ == '__main__':
    # Initialize face colors to all white
    initial_face_colors = {
        "B  ack": ['red'] * 9,
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
