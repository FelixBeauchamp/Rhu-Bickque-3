import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QTabWidget, QPushButton
from PyQt5.QtCore import QTimer


class CubeDisplay(QWidget):
    def __init__(self, cube_faces, parent=None):
        super().__init__(parent)
        self.cube_faces = cube_faces
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setStyleSheet("background-color: cyan;")  # Set background color to cyan

        # Create a grid layout for the faces
        self.grid_layout = QGridLayout()

        # Add faces to the grid layout
        face_positions = [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (3, 1)]
        for idx, position in enumerate(face_positions):
            cube_face_data = self.cube_faces[idx]
            cube_face_widget = CubeFaceDisplay(cube_face_data)
            self.grid_layout.addWidget(cube_face_widget, *position)

        layout.addLayout(self.grid_layout)
        self.setLayout(layout)

    def update_cube_faces(self, new_cube_faces):
        self.cube_faces = new_cube_faces

        # Update the cube face widgets with new data
        for idx, position in enumerate([(0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (3, 1)]):
            cube_face_data = self.cube_faces[idx]
            cube_face_widget = CubeFaceDisplay(cube_face_data)
            self.grid_layout.addWidget(cube_face_widget, *position)


class CubeFaceDisplay(QWidget):
    def __init__(self, cube_face, parent=None):
        super().__init__(parent)
        self.cube_face = cube_face
        self.initUI()

    def initUI(self):
        grid_layout = QGridLayout()

        # Create labels for each segment
        for i, letter in enumerate(self.cube_face):
            color = self.letter_to_color(letter)
            label = QLabel()
            label.setStyleSheet(f"QLabel {{ background-color: {color}; border: 1px solid black; }}")
            label.setFixedSize(50, 50)  # Adjust size as needed
            grid_layout.addWidget(label, i // 3, i % 3)

        self.setLayout(grid_layout)

    @staticmethod
    def letter_to_color(letter):
        color_map = {
            'r': 'red',
            'g': 'green',
            'y': 'yellow',
            'b': 'blue',
            'o': 'orange',
            'w': 'white',
        }
        return color_map.get(letter, 'white')  # Default to white if letter is not found


class ControlsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create a start button
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_function)
        layout.addWidget(self.start_button)

        # Create a stop button
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_function)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def start_function(self):
        # Add code here to trigger the function in another program
        print("Start button clicked!")

    def stop_function(self):
        # Add code here to stop whatever process was started
        print("Stop button clicked!")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Initial cube face data received from another program
    initial_cube_faces_data = [
        ['r', 'g', 'y', 'b', 'o', 'w', 'g', 'y', 'r'],  # Front face
        ['w', 'o', 'b', 'r', 'y', 'g', 'o', 'c', 'r'],  # Top face
        ['o', 'w', 'g', 'r', 'b', 'y', 'p', 'o', 'c'],  # Left face
        ['w', 'r', 'o', 'g', 'b', 'y', 'p', 'o', 'r'],  # Right face
        ['w', 'g', 'o', 'r', 'b', 'y', 'p', 'o', 'c'],  # Bottom face
        ['g', 'r', 'o', 'b', 'y', 'w', 'p', 'o', 'r']   # Back face
    ]

    # Create a tab widget
    tab_widget = QTabWidget()

    # Create the cube display tab
    cube_display_tab = CubeDisplay(initial_cube_faces_data)
    tab_widget.addTab(cube_display_tab, "Cube Display")

    # Create the controls tab
    controls_tab = ControlsTab()
    tab_widget.addTab(controls_tab, "Controls")

    # Set up the main window
    main_window = QWidget()
    main_layout = QVBoxLayout()
    main_layout.addWidget(tab_widget)
    main_window.setLayout(main_layout)
    main_window.setWindowTitle('Cube Display and Controls')
    main_window.show()

    # Function to update cube faces data
    def update_cube_faces_data():
        new_cube_faces_data = [
            ['r', 'o', 'g', 'r', 'o', 'w', 'g', 'b', 'r'],  # Front face
            ['w', 'o', 'b', 'r', 'y', 'g', 'o', 'c', 'r'],  # Top face
            ['o', 'w', 'g', 'r', 'b', 'y', 'p', 'o', 'c'],  # Left face
            ['w', 'r', 'o', 'g', 'b', 'y', 'p', 'o', 'r'],  # Right face
            ['w', 'g', 'o', 'r', 'b', 'y', 'p', 'o', 'c'],  # Bottom face
            ['g', 'r', 'o', 'b', 'y', 'w', 'p', 'o', 'r']   # Back face
        ]
        cube_display_tab.update_cube_faces(new_cube_faces_data)

    # Example of updating cube faces data after 5 seconds
    QTimer.singleShot(5000, update_cube_faces_data)

    sys.exit(app.exec_())