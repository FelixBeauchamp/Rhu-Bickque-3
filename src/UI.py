import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QGridLayout, QVBoxLayout, QTabWidget, QPushButton, QLineEdit
from PyQt5.QtCore import pyqtSignal

class CubeDisplay(QWidget):
    data_changed = pyqtSignal(list)  # Signal to notify data change

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

        # Emit signal with updated data
        self.data_changed.emit(new_cube_faces)


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
    def __init__(self, cube_display, parent=None):
        super().__init__(parent)
        self.cube_display = cube_display
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create line edits and labels for each face
        face_names = ["Front", "Top", "Left", "Right", "Back", "Bottom"]
        self.line_edits = []
        for face_name in face_names:
            label = QLabel(f"Face: {face_name}")
            layout.addWidget(label)
            line_edit = QLineEdit()
            layout.addWidget(line_edit)
            self.line_edits.append(line_edit)

        # Create a button to apply changes
        apply_button = QPushButton('Apply')
        apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(apply_button)

        self.setLayout(layout)

    def apply_changes(self):
        new_cube_faces_data = []
        for idx, line_edit in enumerate(self.line_edits):
            cube_face_data = line_edit.text().strip().split()
            # If line edit is empty, use initial value instead
            if not cube_face_data:
                cube_face_data = initial_cube_faces_data[idx]
            new_cube_faces_data.append(cube_face_data)
            # Clear the line edit
            line_edit.clear()
        self.cube_display.update_cube_faces(new_cube_faces_data)
        self.update_initial_cube_faces(new_cube_faces_data)

    def update_initial_cube_faces(self, new_cube_faces_data):
        for idx, face_data in enumerate(new_cube_faces_data):
            initial_cube_faces_data[idx] = face_data
        print("Updated initial_cube_faces_data:", initial_cube_faces_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Initial cube face data received from another program
    initial_cube_faces_data = [
        ['r', 'g', 'y', 'b', 'o', 'w', 'g', 'y', 'r'],  # Front face
        ['w', 'o', 'b', 'r', 'y', 'g', 'o', 'c', 'r'],  # Left face
        ['o', 'w', 'g', 'r', 'b', 'y', 'p', 'o', 'c'],  # Top face
        ['w', 'r', 'o', 'g', 'b', 'y', 'p', 'o', 'r'],  # Right face
        ['w', 'g', 'o', 'r', 'b', 'y', 'p', 'o', 'c'],  # Back face
        ['g', 'r', 'o', 'b', 'y', 'w', 'p', 'o', 'r']   # Bottom face
    ]

    # Create the cube display
    cube_display = CubeDisplay(initial_cube_faces_data)

    # Create a tab widget
    tab_widget = QTabWidget()

    # Create the cube display tab
    tab_widget.addTab(cube_display, "Cube Display")

    # Create the controls tab
    controls_tab = ControlsTab(cube_display)
    tab_widget.addTab(controls_tab, "Controls")

    # Set up the main window
    main_window = QWidget()
    main_layout = QVBoxLayout()
    main_layout.addWidget(tab_widget)
    main_window.setLayout(main_layout)
    main_window.setWindowTitle('Cube Display and Controls')
    main_window.show()

    sys.exit(app.exec_())