import sys
import time
import control

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QTimer, QTime, Qt, pyqtSignal

SolvingState = 0
stop_pressed = False
clamp = False
mapping = False
Solve = False

mapping_array = [[[0] * 3 for _ in range(3)] for _ in range(6)]
moves_list = []
total_moves = 0


class CubeDisplay(QWidget):
    def __init__(self, initial_colors, parent=None):
        super().__init__(parent)
        self.face_colors = initial_colors  # Store the initial colors of each face
        self.face_buttons = {}
        self.can_change_colors = True  # Flag to control color changes
        self.start_solve_button_clicked = False  # Flag to track if start button has been clicked
        self.elapsed_time = 0  # Variable to store elapsed time
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.setup_faces()
        layout.addLayout(self.grid_layout)

        # Add apply button
        self.apply_button = QPushButton("Apply")
        self.apply_button.setFixedSize(60, 30)  # Set fixed size
        self.apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(self.apply_button, alignment=Qt.AlignHCenter)  # Align button to center

        # Add timer widgets
        self.timer_label = QLabel("Time elapsed: 0:00.00")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.start_clamping_button = QPushButton("Start Clamping")
        self.start_clamping_button.setFixedSize(500, 30)  # Set fixed size
        self.start_clamping_button.clicked.connect(self.start_clamping)
        self.start_mapping_button = QPushButton("Start Mapping")
        self.start_mapping_button.setFixedSize(500, 30)  # Set fixed size
        self.start_mapping_button.clicked.connect(self.start_mapping)
        self.start_solve_button = QPushButton("Start Solve")
        self.start_solve_button.setFixedSize(500, 30)  # Set fixed size
        self.start_solve_button.clicked.connect(self.start_solve)
        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedSize(500, 30)  # Set fixed size
        self.stop_button.clicked.connect(self.stop_timer)
        layout.addWidget(self.timer_label, alignment=Qt.AlignHCenter)  # Align label to center
        layout.addWidget(self.start_clamping_button, alignment=Qt.AlignHCenter)  # Align button to center
        layout.addWidget(self.start_mapping_button, alignment=Qt.AlignHCenter)  # Align button to center
        layout.addWidget(self.start_solve_button, alignment=Qt.AlignHCenter)  # Align button to center
        layout.addWidget(self.stop_button, alignment=Qt.AlignHCenter)  # Align button to center

        # Add progress bar and percentage label
        self.progress_label = QLabel("Progress: 0%")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 120)  # Set the range of the progress bar
        self.progress_bar.setValue(0)  # Start with the progress bar empty
        self.progress_bar.setFixedSize(500, 30)  # Set fixed size
        layout.addWidget(self.progress_bar, alignment=Qt.AlignHCenter)  # Align progress bar to center
        self.setLayout(layout)
        self.start_clamping_button.setEnabled(True)
        self.start_mapping_button.setEnabled(False)
        self.start_solve_button.setEnabled(False)

        time.sleep(0.1)
        control.initialisation()

    def setup_faces(self):
        # Clear any existing widgets
        for i in reversed(range(self.grid_layout.count())):
            layoutItem = self.grid_layout.itemAt(i)
            if layoutItem.widget():
                layoutItem.widget().setParent(None)

        # Define the order of the faces for the cross shape
        face_order = [("Top", 0, 1), ("Left", 1, 0), ("Front", 1, 1), ("Right", 1, 2), ("Bottom", 2, 1), ("Back", 1, 3)]
        for i, (face_name, row, col) in enumerate(face_order):
            face_grid = QGridLayout()
            face_grid.setHorizontalSpacing(0)  # Set spacing between squares to 0
            face_grid.setVerticalSpacing(0)  # Set spacing between squares to 0
            face_colors = self.face_colors[face_name]
            for seg_idx, color in enumerate(face_colors):
                label = QPushButton()
                # label.setProperty("face_name", face_name)
                label.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
                label.setFixedSize(50, 50)
                label.clicked.connect(lambda state, f=face_name, s=seg_idx: self.change_color(f, s))
                face_grid.addWidget(label, seg_idx // 3, seg_idx % 3)
                self.face_buttons[(face_name, seg_idx)] = label
            self.grid_layout.addLayout(face_grid, row, col)

    def change_color(self, face_name, seg_idx):
        if self.can_change_colors:
            color_map = ['white', 'red', 'green', 'yellow', 'blue', 'orange']
            current_color = self.face_colors[face_name][seg_idx]
            next_color = color_map[(color_map.index(current_color) + 1) % len(color_map)]
            self.face_colors[face_name][seg_idx] = next_color
            sender = self.sender()
            sender.setStyleSheet(f"background-color: {next_color}; border: 1px solid black;")

    def apply_changes(self):
        if self.can_change_colors:
            print("Initial face colors array after applying changes:")
            for face_name, colors in self.face_colors.items():
                print(f"{face_name}: {colors}")

    def stop_timer(self):
        if hasattr(self, 'timer'):
            self.timer.stop()
            self.elapsed_time = self.start_time.elapsed()
            self.close()  # Close the UI when stop button is pressed

    def reset_timer(self):
        self.timer_label.setText("Time elapsed: 0:00.00")
        if hasattr(self, 'timer'):
            self.timer.stop()
            self.elapsed_time = 0  # Reset elapsed time
        self.progress_bar.setValue(0)  # Reset progress bar value
        self.progress_label.setText("Progress: 0%")
        self.can_change_colors = True  # Enable color changes
        self.start_solve_button_clicked = False  # Reset start button clicked flag
        self.start_solve_button.setEnabled(True)
        self.apply_button.setEnabled(True)  # Re-enable apply button

    def update_timer(self):
        current_time = QTime.currentTime()
        self.elapsed_time = self.start_time.msecsTo(current_time)
        minutes = self.elapsed_time // 60000
        seconds = (self.elapsed_time % 60000) // 1000
        milliseconds = self.elapsed_time % 1000
        self.timer_label.setText(f"Time elapsed: {minutes}:{seconds:02}.{milliseconds:02}")
        self.timer_label.update()
        QApplication.processEvents()

        # Update progress bar value and percentage label
        # self.progress_bar.setValue(seconds)
        # progress_percent = (seconds / 120) * 100
        # self.progress_label.setText(f"Progress: {progress_percent:.1f}%")

    # Additional methods for start_clamping and start_mapping buttons
    def start_clamping(self):
        self.start_mapping_button.setEnabled(False)
        self.start_mapping_button.setEnabled(False)
        self.start_solve_button.setEnabled(False)
        control.clamp()
        self.start_mapping_button.setEnabled(False)
        self.start_mapping_button.setEnabled(True)
        self.start_solve_button.setEnabled(False)

    def update_face_colors(self, modified_dict):
        if self.can_change_colors:
            face_order = [("Top", 0, 1), ("Left", 1, 0), ("Front", 1, 1), ("Right", 1, 2), ("Bottom", 2, 1),
                          ("Back", 1, 3)]
            for i, (face_name, row, col) in enumerate(face_order):
                face_colors = modified_dict[face_name]
                for seg_idx, color in enumerate(face_colors):
                    next_color = modified_dict[face_name][seg_idx]
                    self.face_colors[face_name][seg_idx] = next_color
                    button = self.face_buttons.get((face_name, seg_idx))
                    if button:
                        button.setStyleSheet(f"background-color: {next_color}; border: 1px solid black;")
                        # Update the stored color in the face_colors dictionary
                        self.face_colors[face_name][seg_idx] = next_color

    def start_mapping(self):
        global mapping_array
        global moves_list

        self.start_mapping_button.setEnabled(False)
        self.start_mapping_button.setEnabled(False)
        self.start_solve_button.setEnabled(False)

        mapping_array = control.mapping_sequence()
        print(mapping_array)
        # Modified dictionnary to show colors on UI
        # Empty dictionary to store the modified array
        modified_dict = {}

        # Define the names of the faces
        face_names = ['Front', 'Right', 'Back', 'Left', 'Bottom', 'Top']

        # Iterate through the input array and convert each list of colors into lists of RGB values
        for i, face_name in enumerate(face_names):
            # Extract three consecutive lists of colors
            face_colors = mapping_array[i]

            # Convert colors to RGB format
            face_rgb = [
                'red' if color == 'R' else 'green' if color == 'G' else 'blue' if color == 'B' else
                'white' if color == 'W' else 'yellow' if color == 'Y' else 'orange' for row in face_colors
                for color in row
            ]

            # Append the converted RGB values to the modified dictionary with the face name as the key
            modified_dict[face_name] = face_rgb

        # Print the modified dictionary
        print(modified_dict)
        self.update_face_colors(modified_dict)
        self.start_mapping_button.setEnabled(False)
        self.start_mapping_button.setEnabled(False)
        self.start_solve_button.setEnabled(True)

    def start_solve(self):
        global moves_list
        self.can_change_colors = False
        self.start_mapping_button.setEnabled(False)
        self.start_mapping_button.setEnabled(False)
        self.start_solve_button.setEnabled(False)

        # Change the mapping array back to its original form after applying manual change
        color_map = {
            'green': 'G',
            'red': 'R',
            'blue': 'B',
            'white': 'W',
            'yellow': 'Y',
            'orange': 'O'
        }
        converted_face_colors = []
        for face_name in ['Front', 'Right', 'Back', 'Left', 'Bottom', 'Top']:
            # Récupérer les couleurs de la face et les convertir selon la carte de couleur
            face_colors = [color_map[color] for color in self.face_colors[face_name]]
            # Diviser les couleurs en sous-tableaux de 3 éléments
            face_subarrays = [face_colors[i:i + 3] for i in range(0, len(face_colors), 3)]
            # Ajouter les sous-tableaux à notre tableau principal
            converted_face_colors.append(face_subarrays)
        moves_list = control.solving_moves(converted_face_colors)
        self.start_time = QTime.currentTime()
        self.timer.start(10)
        print((len(moves_list)))
        i = 0
        for move in moves_list[2]:
            print(move)
            for sub_move in move:
                print(sub_move)
                control.do_move(sub_move)
            self.apply_move(self.face_colors)
            self.can_change_colors = True
            self.update_face_colors(self.face_colors, moves_list[0][i])
            self.can_change_colors = False
            i = i + 1

    def apply_move(self, color_to_change, move):
        # Define the mapping of faces affected by each move
        move_mapping = {
            'L': [('Left', (0, 0), (1, 0), (2, 0)),
                  ('Front', (0, 0), (1, 0), (2, 0)),
                  ('Right', (0, 0), (1, 0), (2, 0)),
                  ('Back', (0, 0), (1, 0), (2, 0)),
                  ('Top', (0, 0), (1, 0), (2, 0)),
                  ('Bottom', (0, 0), (1, 0), (2, 0))],
            'R': [('Right', (0, 2), (1, 2), (2, 2)),
                  ('Front', (0, 2), (1, 2), (2, 2)),
                  ('Left', (0, 2), (1, 2), (2, 2)),
                  ('Back', (0, 2), (1, 2), (2, 2)),
                  ('Top', (0, 2), (1, 2), (2, 2)),
                  ('Bottom', (0, 2), (1, 2), (2, 2))],
            'U': [('Top', (0, 0), (0, 1), (0, 2)),
                  ('Front', (0, 0), (0, 1), (0, 2)),
                  ('Right', (0, 0), (0, 1), (0, 2)),
                  ('Back', (0, 0), (0, 1), (0, 2)),
                  ('Left', (0, 0), (0, 1), (0, 2)),
                  ('Bottom', (0, 0), (0, 1), (0, 2))],
            'D': [('Bottom', (0, 0), (0, 1), (0, 2)),
                  ('Front', (2, 0), (2, 1), (2, 2)),
                  ('Right', (2, 0), (2, 1), (2, 2)),
                  ('Back', (2, 0), (2, 1), (2, 2)),
                  ('Left', (2, 0), (2, 1), (2, 2)),
                  ('Top', (0, 0), (0, 1), (0, 2))],
            'F': [('Front', (0, 0), (0, 1), (0, 2)),
                  ('Right', (0, 0), (1, 0), (2, 0)),
                  ('Back', (2, 2), (2, 1), (2, 0)),
                  ('Left', (0, 2), (1, 2), (2, 2)),
                  ('Top', (2, 0), (2, 1), (2, 2)),
                  ('Bottom', (0, 0), (0, 1), (0, 2))],
            'B': [('Back', (0, 0), (0, 1), (0, 2)),
                  ('Right', (0, 2), (1, 2), (2, 2)),
                  ('Front', (2, 2), (2, 1), (2, 0)),
                  ('Left', (0, 0), (1, 0), (2, 0)),
                  ('Top', (0, 0), (0, 1), (0, 2)),
                  ('Bottom', (2, 0), (2, 1), (2, 2))],
            "Li": [('Left', (2, 0), (1, 0), (0, 0)),
                   ('Front', (2, 0), (1, 0), (0, 0)),
                   ('Right', (2, 0), (1, 0), (0, 0)),
                   ('Back', (2, 0), (1, 0), (0, 0)),
                   ('Top', (2, 0), (1, 0), (0, 0)),
                   ('Bottom', (2, 0), (1, 0), (0, 0))],
            "Ri": [('Right', (2, 2), (1, 2), (0, 2)),
                   ('Front', (0, 2), (1, 2), (2, 2)),
                   ('Left', (2, 2), (1, 2), (0, 2)),
                   ('Back', (0, 2), (1, 2), (2, 2)),
                   ('Top', (0, 2), (1, 2), (2, 2)),
                   ('Bottom', (0, 2), (1, 2), (2, 2))],
            "Ui": [('Top', (0, 2), (0, 1), (0, 0)),
                   ('Front', (0, 2), (0, 1), (0, 0)),
                   ('Right', (0, 2), (0, 1), (0, 0)),
                   ('Back', (0, 2), (0, 1), (0, 0)),
                   ('Left', (0, 2), (0, 1), (0, 0)),
                   ('Bottom', (0, 2), (0, 1), (0, 0))],
            "Di": [('Bottom', (0, 2), (0, 1), (0, 0)),
                   ('Front', (0, 0), (0, 1), (0, 2)),
                   ('Right', (0, 0), (0, 1), (0, 2)),
                   ('Back', (0, 0), (0, 1), (0, 2)),
                   ('Left', (0, 0), (0, 1), (0, 2)),
                   ('Top', (0, 0), (0, 1), (0, 2))],
            "Fi": [('Front', (0, 2), (0, 1), (0, 0)),
                   ('Right', (0, 2), (1, 2), (2, 2)),
                   ('Back', (2, 0), (2, 1), (2, 2)),
                   ('Left', (0, 0), (1, 0), (2, 0)),
                   ('Top', (0, 2), (0, 1), (0, 0)),
                   ('Bottom', (0, 2), (0, 1), (0, 0))],
            "Bi'": [('Back', (0, 2), (0, 1), (0, 0)),
                    ('Right', (0, 0), (1, 0), (2, 0)),
                    ('Front', (2, 0), (2, 1), (2, 2)),
                    ('Left', (0, 2), (1, 2), (2, 2)),
                    ('Top', (0, 0), (0, 1), (0, 2)),
                    ('Bottom', (0, 0), (0, 1), (0, 2))],
            'M': [('Right', (0, 1), (1, 1), (2, 1)),
                  ('Front', (0, 1), (1, 1), (2, 1)),
                  ('Left', (0, 1), (1, 1), (2, 1)),
                  ('Back', (0, 1), (1, 1), (2, 1)),
                  ('Top', (0, 1), (1, 1), (2, 1)),
                  ('Bottom', (0, 1), (1, 1), (2, 1))],
            'E': [('Top', (1, 0), (1, 1), (1, 2)),
                  ('Front', (1, 0), (1, 1), (1, 2)),
                  ('Right', (1, 0), (1, 1), (1, 2)),
                  ('Back', (1, 0), (1, 1), (1, 2)),
                  ('Left', (1, 0), (1, 1), (1, 2)),
                  ('Bottom', (1, 0), (1, 1), (1, 2))],
            'S': [('Front', (1, 0), (1, 1), (1, 2)),
                  ('Right', (1, 0), (1, 1), (1, 2)),
                  ('Back', (1, 0), (1, 1), (1, 2)),
                  ('Left', (1, 0), (1, 1), (1, 2)),
                  ('Top', (1, 0), (1, 1), (1, 2)),
                  ('Bottom', (1, 0), (1, 1), (1, 2))],
            "Mi": [('Right', (2, 1), (1, 1), (0, 1)),
                   ('Front', (2, 1), (1, 1), (0, 1)),
                   ('Left', (2, 1), (1, 1), (0, 1)),
                   ('Back', (2, 1), (1, 1), (0, 1)),
                   ('Top', (2, 1), (1, 1), (0, 1)),
                   ('Bottom', (2, 1), (1, 1), (0, 1))],
            "Ei": [('Top', (1, 2), (1, 1), (1, 0)),
                   ('Front', (1, 2), (1, 1), (1, 0)),
                   ('Right', (1, 2), (1, 1), (1, 0)),
                   ('Back', (1, 2), (1, 1), (1, 0)),
                   ('Left', (1, 2), (1, 1), (1, 0)),
                   ('Bottom', (1, 2), (1, 1), (1, 0))],
            "Si": [('Front', (1, 2), (1, 1), (1, 0)),
                   ('Right', (1, 2), (1, 1), (1, 0)),
                   ('Back', (1, 2), (1, 1), (1, 0)),
                   ('Left', (1, 2), (1, 1), (1, 0)),
                   ('Top', (1, 2), (1, 1), (1, 0)),
                   ('Bottom', (1, 2), (1, 1), (1, 0))],
            'l': [('Left', (0, 0), (1, 0), (2, 0)),
                  ('Front', (0, 0), (1, 0), (2, 0)),
                  ('Top', (0, 0), (1, 0), (2, 0)),
                  ('Back', (0, 0), (1, 0), (2, 0)),
                  ('Bottom', (0, 0), (1, 0), (2, 0)),
                  ('Right', (0, 2), (1, 2), (2, 2))],
            'r': [('Right', (0, 2), (1, 2), (2, 2)),
                  ('Front', (0, 2), (1, 2), (2, 2)),
                  ('Top', (0, 2), (1, 2), (2, 2)),
                  ('Back', (0, 2), (1, 2), (2, 2)),
                  ('Bottom', (0, 2), (1, 2), (2, 2)),
                  ('Left', (0, 0), (1, 0), (2, 0))],
            'u': [('Top', (0, 0), (0, 1), (0, 2)),
                  ('Front', (0, 0), (0, 1), (0, 2)),
                  ('Right', (0, 0), (0, 1), (0, 2)),
                  ('Back', (0, 0), (0, 1), (0, 2)),
                  ('Left', (0, 0), (0, 1), (0, 2)),
                  ('Bottom', (2, 0), (2, 1), (2, 2))],
            'd': [('Bottom', (0, 0), (0, 1), (0, 2)),
                  ('Front', (2, 0), (2, 1), (2, 2)),
                  ('Right', (2, 0), (2, 1), (2, 2)),
                  ('Back', (2, 0), (2, 1), (2, 2)),
                  ('Left', (2, 0), (2, 1), (2, 2)),
                  ('Top', (0, 0), (0, 1), (0, 2))],
            'f': [('Front', (0, 0), (0, 1), (0, 2)),
                  ('Right', (0, 0), (0, 1), (0, 2)),
                  ('Top', (0, 0), (0, 1), (0, 2)),
                  ('Bottom', (0, 0), (0, 1), (0, 2)),
                  ('Back', (0, 0), (0, 1), (0, 2)),
                  ('Left', (0, 0), (0, 1), (0, 2))],
            'b': [('Back', (0, 0), (0, 1), (0, 2)),
                  ('Right', (2, 0), (2, 1), (2, 2)),
                  ('Top', (0, 2), (0, 1), (0, 0)),
                  ('Bottom', (0, 2), (0, 1), (0, 0)),
                  ('Left', (2, 0), (2, 1), (2, 2)),
                  ('Front', (2, 0), (2, 1), (2, 2))],
            'li': [('Right', (0, 2), (1, 2), (2, 2)),
                   ('Back', (0, 0), (1, 0), (2, 0)),
                   ('Top', (0, 0), (1, 0), (2, 0)),
                   ('Front', (0, 0), (1, 0), (2, 0)),
                   ('Bottom', (0, 0), (1, 0), (2, 0)),
                   ('Left', (0, 0), (1, 0), (2, 0))],
            'ri': [('Left', (0, 0), (1, 0), (2, 0)),
                   ('Back', (0, 2), (1, 2), (2, 2)),
                   ('Top', (0, 2), (1, 2), (2, 2)),
                   ('Front', (0, 2), (1, 2), (2, 2)),
                   ('Bottom', (0, 2), (1, 2), (2, 2)),
                   ('Right', (0, 0), (1, 0), (2, 0))],
            'ui': [('Bottom', (2, 0), (2, 1), (2, 2)),
                   ('Left', (0, 0), (0, 1), (0, 2)),
                   ('Back', (0, 0), (0, 1), (0, 2)),
                   ('Front', (0, 0), (0, 1), (0, 2)),
                   ('Right', (0, 0), (0, 1), (0, 2)),
                   ('Top', (0, 0), (0, 1), (0, 2))],
            'di': [('Top', (0, 0), (0, 1), (0, 2)),
                   ('Left', (2, 0), (2, 1), (2, 2)),
                   ('Back', (2, 0), (2, 1), (2, 2)),
                   ('Front', (2, 0), (2, 1), (2, 2)),
                   ('Right', (2, 0), (2, 1), (2, 2)),
                   ('Bottom', (0, 0), (0, 1), (0, 2))],
            'fi': [('Back', (0, 0), (0, 1), (0, 2)),
                   ('Right', (0, 0), (0, 1), (0, 2)),
                   ('Bottom', (0, 0), (0, 1), (0, 2)),
                   ('Top', (0, 0), (0, 1), (0, 2)),
                   ('Left', (0, 0), (0, 1), (0, 2)),
                   ('Front', (0, 0), (0, 1), (0, 2))],
            'bi': [('Front', (0, 0), (0, 1), (0, 2)),
                   ('Right', (2, 0), (2, 1), (2, 2)),
                   ('Bottom', (0, 2), (0, 1), (0, 0)),
                   ('Top', (0, 2), (0, 1), (0, 0)),
                   ('Left', (2, 0), (2, 1), (2, 2)),
                   ('Back', (2, 0), (2, 1), (2, 2))]
        }

        # Apply the move to the face colors dictionary
        for face, *positions in move_mapping[move]:
            face_color = color_to_change[face]
            colors = [face_color[pos[0]][pos[1]] for pos in positions]
            new_colors = colors[-1:] + colors[:-1]  # Shift the colors
            for pos, color in zip(positions, new_colors):
                face_color[pos[0]][pos[1]] = color

# if __name__ == '__main__':
# # Initialize face colors to all white
# initial_face_colors = {
#     "Back": ['red'] * 9,
#     "Left": ['green'] * 9,
#     "Top": ['yellow'] * 9,
#     "Right": ['blue'] * 9,
#     "Front": ['orange'] * 9,
#     "Bottom": ['white'] * 9
# }
#
# app = QApplication(sys.argv)
# cube_display = CubeDisplay(initial_face_colors)
# cube_display.show()
#
# sys.exit(app.exec_())
