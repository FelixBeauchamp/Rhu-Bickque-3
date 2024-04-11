import sys
import time
import control
import pygame

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QTimer, QTime, Qt, pyqtSignal
from PyQt5.QtCore import QObject, QEvent

mapping_array = [[[0] * 3 for _ in range(3)] for _ in range(6)]
moves_list = []
total_moves = 0
stop_flag = False


class CubeDisplay(QWidget):
    def __init__(self, initial_colors, parent=None):
        super().__init__(parent)
        self.start_time = None
        self.face_colors = initial_colors  # Store the initial colors of each face
        self.face_buttons = {}
        self.can_change_colors = True  # Flag to control color changes
        self.start_solve_button_clicked = False  # Flag to track if start button has been clicked
        self.elapsed_time = 0  # Variable to store elapsed time
        self.initUI()
        self.actual_move = 0
        self.total_moves = 0
        self.can_clamp = True
        self.can_map = False
        self.can_solve = False
        self.audio_timer = QTimer()
        self.audio_timer.timeout.connect(self.play_audio_file)

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
        self.timer_label = QLabel("Time elapsed: 0:00")
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
        self.stop_button.clicked.connect(self.stop)
        layout.addWidget(self.timer_label, alignment=Qt.AlignHCenter)  # Align label to center
        layout.addWidget(self.start_clamping_button, alignment=Qt.AlignHCenter)  # Align button to center
        layout.addWidget(self.start_mapping_button, alignment=Qt.AlignHCenter)  # Align button to center
        layout.addWidget(self.start_solve_button, alignment=Qt.AlignHCenter)  # Align button to center
        layout.addWidget(self.stop_button, alignment=Qt.AlignHCenter)  # Align button to center

        # Add progress bar and percentage label
        self.progress_label = QLabel("Progress: 0%")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)  # Set the range of the progress bar
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
            # print("Initial face colors array after applying changes:")
            for face_name, colors in self.face_colors.items():
                # print(f"{face_name}: {colors}")

    def stop(self):
        global stop_flag
        stop_flag = True
        QApplication.quit()
        sys.exit(0)

    def stop_timer(self):
        if hasattr(self, 'timer'):
            self.timer.stop()
            self.elapsed_time = self.start_time.elapsed()
            # self.close()  # Close the UI when stop button is pressed

    def reset_timer(self):
        self.timer_label.setText("Time elapsed: 0:00")
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
        # milliseconds = self.elapsed_time % 1000
        # self.timer_label.setText(f"Time elapsed: {minutes}:{seconds:02}.{milliseconds:02}")
        self.timer_label.setText(f"Time elapsed: {minutes}:{seconds:02}")
        self.timer_label.update()
        QApplication.processEvents()

        # Update progress bar value and percentage label
        self.progress_bar.setValue(self.actual_move)
        progress_percent = (self.actual_move / self.total_moves) * 100
        self.progress_label.setText(f"Progress: {progress_percent:.1f}%")

    def disable_buttons(self):
        self.start_clamping_button.setEnabled(False)
        self.start_mapping_button.setEnabled(False)
        self.start_solve_button.setEnabled(False)

    def enable_buttons(self):

        self.start_clamping_button.setEnabled(self.can_clamp)
        self.start_mapping_button.setEnabled(self.can_map)
        self.start_solve_button.setEnabled(self.can_solve)

    # Additional methods for start_clamping and start_mapping buttons
    def start_clamping(self):
        if not self.can_clamp:
            return
        self.disable_buttons()
        self.start_clamping_button.setEnabled(False)
        self.start_mapping_button.setEnabled(False)
        self.start_solve_button.setEnabled(False)
        control.clamp()
        self.start_clamping_button.setEnabled(False)
        self.start_mapping_button.setEnabled(True)
        self.start_solve_button.setEnabled(False)
        self.can_map = True
        self.can_clamp = False
        self.enable_buttons()

    def update_face_colors(self, modified_dict):
        # print('Starting UI update')
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
        return True
        # print('The Ui is now updated')

    def start_mapping(self):
        global mapping_array
        global moves_list
        if not self.can_map:
            return
        self.disable_buttons()
        self.start_clamping_button.setEnabled(False)
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
        self.start_clamping_button.setEnabled(False)
        self.start_mapping_button.setEnabled(False)
        self.start_solve_button.setEnabled(True)
        self.can_solve = True
        self.can_map = False
        self.enable_buttons()

    def start_solve(self):
        global moves_list
        global stop_flag

        if not self.can_solve:
            return
        self.disable_buttons()
        stop_flag = False
        self.can_change_colors = False
        self.start_clamping_button.setEnabled(False)
        self.start_mapping_button.setEnabled(False)
        self.start_solve_button.setEnabled(False)
        self.can_solve = False

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
        self.total_moves = len(moves_list[1])
        self.progress_bar.setRange(0, self.total_moves)
        self.start_time = QTime.currentTime()
        self.timer.start(10)
        self.update_timer()
        i = 0
        self.can_change_colors = True
        for move in moves_list[2]:
            print(moves_list[0][i])
            self.apply_move(moves_list[0][i])
            for sub_move in move:
                control.do_move(sub_move)
                self.update_timer()
                self.actual_move = self.actual_move + 1
            self.update_face_colors(self.face_colors)
            i = i + 1
        self.update_face_colors(self.face_colors)
        self.stop_timer()
        self.audio_timer.start(1000)
        print('Done solving')
        self.can_change_colors = False

    def apply_move(self, move):
        # print('Applying move')
        if move == 'R':
            temp_top = [self.face_colors['Top'][2], self.face_colors['Top'][5], self.face_colors['Top'][8]]
            temp_front = [self.face_colors['Front'][2], self.face_colors['Front'][5], self.face_colors['Front'][8]]
            temp_bottom = [self.face_colors['Bottom'][2], self.face_colors['Bottom'][5], self.face_colors['Bottom'][8]]
            temp_back = [self.face_colors['Back'][0], self.face_colors['Back'][3], self.face_colors['Back'][6]]

            self.face_colors['Back'][0], self.face_colors['Back'][3], self.face_colors['Back'][6] = temp_top[::-1]
            self.face_colors['Top'][2], self.face_colors['Top'][5], self.face_colors['Top'][8] = temp_front
            self.face_colors['Front'][2], self.face_colors['Front'][5], self.face_colors['Front'][8] = temp_bottom
            self.face_colors['Bottom'][2], self.face_colors['Bottom'][5], self.face_colors['Bottom'][8] = temp_back[
                                                                                                          ::-1]

            # # Rotation de la face droite dans le sens horaire
            self.face_colors['Right'][0], self.face_colors['Right'][1], self.face_colors['Right'][2], \
                self.face_colors['Right'][3], self.face_colors['Right'][4], self.face_colors['Right'][5], \
                self.face_colors['Right'][6], self.face_colors['Right'][7], self.face_colors['Right'][8] = \
                self.face_colors['Right'][6], self.face_colors['Right'][3], self.face_colors['Right'][0], \
                    self.face_colors['Right'][7], self.face_colors['Right'][4], self.face_colors['Right'][1], \
                    self.face_colors['Right'][8], self.face_colors['Right'][5], self.face_colors['Right'][2]

        elif move == "Ri":
            self.apply_move('R')
            self.apply_move('R')
            self.apply_move('R')
        elif move == 'duoR' or move == 'duoRi':
            self.apply_move('R')
            self.apply_move('R')

        elif move == 'r':
            temp_top = [self.face_colors['Top'][2], self.face_colors['Top'][5], self.face_colors['Top'][8]]
            temp_front = [self.face_colors['Front'][2], self.face_colors['Front'][5], self.face_colors['Front'][8]]
            temp_bottom = [self.face_colors['Bottom'][2], self.face_colors['Bottom'][5], self.face_colors['Bottom'][8]]
            temp_back = [self.face_colors['Back'][0], self.face_colors['Back'][3], self.face_colors['Back'][6]]
            temp_top_2 = [self.face_colors['Top'][1], self.face_colors['Top'][4], self.face_colors['Top'][7]]
            temp_front_2 = [self.face_colors['Front'][1], self.face_colors['Front'][4], self.face_colors['Front'][7]]
            temp_bottom_2 = [self.face_colors['Bottom'][1], self.face_colors['Bottom'][4],
                             self.face_colors['Bottom'][7]]
            temp_back_2 = [self.face_colors['Back'][1], self.face_colors['Back'][4], self.face_colors['Back'][7]]

            self.face_colors['Back'][0], self.face_colors['Back'][3], self.face_colors['Back'][6] = temp_top[::-1]
            self.face_colors['Top'][2], self.face_colors['Top'][5], self.face_colors['Top'][8] = temp_front
            self.face_colors['Front'][2], self.face_colors['Front'][5], self.face_colors['Front'][8] = temp_bottom
            self.face_colors['Bottom'][2], self.face_colors['Bottom'][5], self.face_colors['Bottom'][8] = temp_back[
                                                                                                          ::-1]
            self.face_colors['Back'][1], self.face_colors['Back'][4], self.face_colors['Back'][7] = temp_top_2[::-1]
            self.face_colors['Top'][1], self.face_colors['Top'][4], self.face_colors['Top'][7] = temp_front_2
            self.face_colors['Front'][1], self.face_colors['Front'][4], self.face_colors['Front'][7] = temp_bottom_2
            self.face_colors['Bottom'][1], self.face_colors['Bottom'][4], self.face_colors['Bottom'][7] = temp_back_2[
                                                                                                          ::-1]
            # # Rotation de la face droite dans le sens horaire
            self.face_colors['Right'][0], self.face_colors['Right'][1], self.face_colors['Right'][2], \
                self.face_colors['Right'][3], self.face_colors['Right'][4], self.face_colors['Right'][5], \
                self.face_colors['Right'][6], self.face_colors['Right'][7], self.face_colors['Right'][8] = \
                self.face_colors['Right'][6], self.face_colors['Right'][3], self.face_colors['Right'][0], \
                    self.face_colors['Right'][7], self.face_colors['Right'][4], self.face_colors['Right'][1], \
                    self.face_colors['Right'][8], self.face_colors['Right'][5], self.face_colors['Right'][2]

        elif move == "ri":
            self.apply_move('r')
            self.apply_move('r')
            self.apply_move('r')
        elif move == 'duor' or move == 'duori':
            self.apply_move('r')
            self.apply_move('r')

        elif move == 'L':
            temp_top = [self.face_colors['Top'][0], self.face_colors['Top'][3], self.face_colors['Top'][6]]
            temp_front = [self.face_colors['Front'][0], self.face_colors['Front'][3], self.face_colors['Front'][6]]
            temp_bottom = [self.face_colors['Bottom'][0], self.face_colors['Bottom'][3], self.face_colors['Bottom'][6]]
            temp_back = [self.face_colors['Back'][2], self.face_colors['Back'][5], self.face_colors['Back'][8]]

            self.face_colors['Back'][2], self.face_colors['Back'][5], self.face_colors['Back'][8] = temp_bottom[::-1]
            self.face_colors['Top'][0], self.face_colors['Top'][3], self.face_colors['Top'][6] = temp_back[::-1]
            self.face_colors['Front'][0], self.face_colors['Front'][3], self.face_colors['Front'][6] = temp_top
            self.face_colors['Bottom'][0], self.face_colors['Bottom'][3], self.face_colors['Bottom'][6] = temp_front

            # # Rotation de la face droite dans le sens horaire
            self.face_colors['Left'][0], self.face_colors['Left'][1], self.face_colors['Left'][2], \
                self.face_colors['Left'][3], self.face_colors['Left'][4], self.face_colors['Left'][5], \
                self.face_colors['Left'][6], self.face_colors['Left'][7], self.face_colors['Left'][8] = \
                self.face_colors['Left'][6], self.face_colors['Left'][3], self.face_colors['Left'][0], \
                    self.face_colors['Left'][7], self.face_colors['Left'][4], self.face_colors['Left'][1], \
                    self.face_colors['Left'][8], self.face_colors['Left'][5], self.face_colors['Left'][2]
        elif move == "Li":
            self.apply_move('L')
            self.apply_move('L')
            self.apply_move('L')
        elif move == 'duoL' or move == 'duoLi':
            self.apply_move('L')
            self.apply_move('L')

        elif move == 'l':
            temp_top = [self.face_colors['Top'][0], self.face_colors['Top'][3], self.face_colors['Top'][6]]
            temp_front = [self.face_colors['Front'][0], self.face_colors['Front'][3], self.face_colors['Front'][6]]
            temp_bottom = [self.face_colors['Bottom'][0], self.face_colors['Bottom'][3], self.face_colors['Bottom'][6]]
            temp_back = [self.face_colors['Back'][2], self.face_colors['Back'][5], self.face_colors['Back'][8]]
            temp_top_2 = [self.face_colors['Top'][1], self.face_colors['Top'][4], self.face_colors['Top'][7]]
            temp_front_2 = [self.face_colors['Front'][1], self.face_colors['Front'][4], self.face_colors['Front'][7]]
            temp_bottom_2 = [self.face_colors['Bottom'][1], self.face_colors['Bottom'][4],
                             self.face_colors['Bottom'][7]]
            temp_back_2 = [self.face_colors['Back'][1], self.face_colors['Back'][4], self.face_colors['Back'][7]]

            self.face_colors['Back'][2], self.face_colors['Back'][5], self.face_colors['Back'][8] = temp_bottom[::-1]
            self.face_colors['Top'][0], self.face_colors['Top'][3], self.face_colors['Top'][6] = temp_back[::-1]
            self.face_colors['Front'][0], self.face_colors['Front'][3], self.face_colors['Front'][6] = temp_top
            self.face_colors['Bottom'][0], self.face_colors['Bottom'][3], self.face_colors['Bottom'][6] = temp_front
            self.face_colors['Back'][1], self.face_colors['Back'][4], self.face_colors['Back'][7] = temp_bottom_2[::-1]
            self.face_colors['Top'][1], self.face_colors['Top'][4], self.face_colors['Top'][7] = temp_back_2[::-1]
            self.face_colors['Front'][1], self.face_colors['Front'][4], self.face_colors['Front'][7] = temp_top_2
            self.face_colors['Bottom'][1], self.face_colors['Bottom'][4], self.face_colors['Bottom'][7] = temp_front_2
            # # Rotation de la face droite dans le sens horaire
            self.face_colors['Left'][0], self.face_colors['Left'][1], self.face_colors['Left'][2], \
                self.face_colors['Left'][3], self.face_colors['Left'][4], self.face_colors['Left'][5], \
                self.face_colors['Left'][6], self.face_colors['Left'][7], self.face_colors['Left'][8] = \
                self.face_colors['Left'][6], self.face_colors['Left'][3], self.face_colors['Left'][0], \
                    self.face_colors['Left'][7], self.face_colors['Left'][4], self.face_colors['Left'][1], \
                    self.face_colors['Left'][8], self.face_colors['Left'][5], self.face_colors['Left'][2]

        elif move == "li":
            self.apply_move('l')
            self.apply_move('l')
            self.apply_move('l')
        elif move == 'duol' or move == 'duoli':
            self.apply_move('l')
            self.apply_move('l')

        elif move == 'U':
            temp_right = [self.face_colors['Right'][0], self.face_colors['Right'][1], self.face_colors['Right'][2]]
            temp_front = [self.face_colors['Front'][0], self.face_colors['Front'][1], self.face_colors['Front'][2]]
            temp_left = [self.face_colors['Left'][0], self.face_colors['Left'][1], self.face_colors['Left'][2]]
            temp_back = [self.face_colors['Back'][0], self.face_colors['Back'][1], self.face_colors['Back'][2]]

            self.face_colors['Right'][0], self.face_colors['Right'][1], self.face_colors['Right'][2] = temp_back
            self.face_colors['Front'][0], self.face_colors['Front'][1], self.face_colors['Front'][2] = temp_right
            self.face_colors['Left'][0], self.face_colors['Left'][1], self.face_colors['Left'][2] = temp_front
            self.face_colors['Back'][0], self.face_colors['Back'][1], self.face_colors['Back'][2] = temp_left

            # # Rotation de la face droite dans le sens horaire
            self.face_colors['Top'][0], self.face_colors['Top'][1], self.face_colors['Top'][2], \
                self.face_colors['Top'][3], self.face_colors['Top'][4], self.face_colors['Top'][5], \
                self.face_colors['Top'][6], self.face_colors['Top'][7], self.face_colors['Top'][8] = \
                self.face_colors['Top'][6], self.face_colors['Top'][3], self.face_colors['Top'][0], \
                    self.face_colors['Top'][7], self.face_colors['Top'][4], self.face_colors['Top'][1], \
                    self.face_colors['Top'][8], self.face_colors['Top'][5], self.face_colors['Top'][2]
        elif move == "Ui":
            self.apply_move('U')
            self.apply_move('U')
            self.apply_move('U')
        elif move == 'duoU' or move == 'duoUi':
            self.apply_move('U')
            self.apply_move('U')

        elif move == 'u':
            temp_right = [self.face_colors['Right'][0], self.face_colors['Right'][1], self.face_colors['Right'][2]]
            temp_front = [self.face_colors['Front'][0], self.face_colors['Front'][1], self.face_colors['Front'][2]]
            temp_left = [self.face_colors['Left'][0], self.face_colors['Left'][1], self.face_colors['Left'][2]]
            temp_back = [self.face_colors['Back'][0], self.face_colors['Back'][1], self.face_colors['Back'][2]]
            temp_right_2 = [self.face_colors['Right'][3], self.face_colors['Right'][4], self.face_colors['Right'][5]]
            temp_front_2 = [self.face_colors['Front'][3], self.face_colors['Front'][4], self.face_colors['Front'][5]]
            temp_left_2 = [self.face_colors['Left'][3], self.face_colors['Left'][4], self.face_colors['Left'][5]]
            temp_back_2 = [self.face_colors['Back'][3], self.face_colors['Back'][4], self.face_colors['Back'][5]]

            self.face_colors['Right'][0], self.face_colors['Right'][1], self.face_colors['Right'][2] = temp_back
            self.face_colors['Front'][0], self.face_colors['Front'][1], self.face_colors['Front'][2] = temp_right
            self.face_colors['Left'][0], self.face_colors['Left'][1], self.face_colors['Left'][2] = temp_front
            self.face_colors['Back'][0], self.face_colors['Back'][1], self.face_colors['Back'][2] = temp_left
            self.face_colors['Right'][3], self.face_colors['Right'][4], self.face_colors['Right'][5] = temp_back_2
            self.face_colors['Front'][3], self.face_colors['Front'][4], self.face_colors['Front'][5] = temp_right_2
            self.face_colors['Left'][3], self.face_colors['Left'][4], self.face_colors['Left'][5] = temp_front_2
            self.face_colors['Back'][3], self.face_colors['Back'][4], self.face_colors['Back'][5] = temp_left_2

            # # Rotation de la face droite dans le sens horaire
            self.face_colors['Top'][0], self.face_colors['Top'][1], self.face_colors['Top'][2], \
                self.face_colors['Top'][3], self.face_colors['Top'][4], self.face_colors['Top'][5], \
                self.face_colors['Top'][6], self.face_colors['Top'][7], self.face_colors['Top'][8] = \
                self.face_colors['Top'][6], self.face_colors['Top'][3], self.face_colors['Top'][0], \
                    self.face_colors['Top'][7], self.face_colors['Top'][4], self.face_colors['Top'][1], \
                    self.face_colors['Top'][8], self.face_colors['Top'][5], self.face_colors['Top'][2]
        elif move == "ui":
            self.apply_move('u')
            self.apply_move('u')
            self.apply_move('u')
        elif move == 'duou' or move == 'duoui':
            self.apply_move('u')
            self.apply_move('u')

        elif move == 'D':
            temp_right = [self.face_colors['Right'][6], self.face_colors['Right'][7], self.face_colors['Right'][8]]
            temp_front = [self.face_colors['Front'][6], self.face_colors['Front'][7], self.face_colors['Front'][8]]
            temp_left = [self.face_colors['Left'][6], self.face_colors['Left'][7], self.face_colors['Left'][8]]
            temp_back = [self.face_colors['Back'][6], self.face_colors['Back'][7], self.face_colors['Back'][8]]

            self.face_colors['Right'][6], self.face_colors['Right'][7], self.face_colors['Right'][8] = temp_front
            self.face_colors['Front'][6], self.face_colors['Front'][7], self.face_colors['Front'][8] = temp_left
            self.face_colors['Left'][6], self.face_colors['Left'][7], self.face_colors['Left'][8] = temp_back
            self.face_colors['Back'][6], self.face_colors['Back'][7], self.face_colors['Back'][8] = temp_right

            # # Rotation de la face droite dans le sens horaire
            self.face_colors['Bottom'][0], self.face_colors['Bottom'][1], self.face_colors['Bottom'][2], \
                self.face_colors['Bottom'][3], self.face_colors['Bottom'][4], self.face_colors['Bottom'][5], \
                self.face_colors['Bottom'][6], self.face_colors['Bottom'][7], self.face_colors['Bottom'][8] = \
                self.face_colors['Bottom'][6], self.face_colors['Bottom'][3], self.face_colors['Bottom'][0], \
                    self.face_colors['Bottom'][7], self.face_colors['Bottom'][4], self.face_colors['Bottom'][1], \
                    self.face_colors['Bottom'][8], self.face_colors['Bottom'][5], self.face_colors['Bottom'][2]
        elif move == "Di":
            self.apply_move('D')
            self.apply_move('D')
            self.apply_move('D')
        elif move == 'duoD' or move == 'duoDi':
            self.apply_move('D')
            self.apply_move('D')

        elif move == 'd':
            temp_right = [self.face_colors['Right'][6], self.face_colors['Right'][7], self.face_colors['Right'][8]]
            temp_front = [self.face_colors['Front'][6], self.face_colors['Front'][7], self.face_colors['Front'][8]]
            temp_left = [self.face_colors['Left'][6], self.face_colors['Left'][7], self.face_colors['Left'][8]]
            temp_back = [self.face_colors['Back'][6], self.face_colors['Back'][7], self.face_colors['Back'][8]]
            temp_right_2 = [self.face_colors['Right'][3], self.face_colors['Right'][4], self.face_colors['Right'][5]]
            temp_front_2 = [self.face_colors['Front'][3], self.face_colors['Front'][4], self.face_colors['Front'][5]]
            temp_left_2 = [self.face_colors['Left'][3], self.face_colors['Left'][4], self.face_colors['Left'][5]]
            temp_back_2 = [self.face_colors['Back'][3], self.face_colors['Back'][4], self.face_colors['Back'][5]]

            self.face_colors['Right'][6], self.face_colors['Right'][7], self.face_colors['Right'][8] = temp_front
            self.face_colors['Front'][6], self.face_colors['Front'][7], self.face_colors['Front'][8] = temp_left
            self.face_colors['Left'][6], self.face_colors['Left'][7], self.face_colors['Left'][8] = temp_back
            self.face_colors['Back'][6], self.face_colors['Back'][7], self.face_colors['Back'][8] = temp_right
            self.face_colors['Right'][3], self.face_colors['Right'][4], self.face_colors['Right'][5] = temp_front_2
            self.face_colors['Front'][3], self.face_colors['Front'][4], self.face_colors['Front'][5] = temp_left_2
            self.face_colors['Left'][3], self.face_colors['Left'][4], self.face_colors['Left'][5] = temp_back_2
            self.face_colors['Back'][3], self.face_colors['Back'][4], self.face_colors['Back'][5] = temp_right_2

            # # Rotation de la face droite dans le sens horaire
            self.face_colors['Bottom'][0], self.face_colors['Bottom'][1], self.face_colors['Bottom'][2], \
                self.face_colors['Bottom'][3], self.face_colors['Bottom'][4], self.face_colors['Bottom'][5], \
                self.face_colors['Bottom'][6], self.face_colors['Bottom'][7], self.face_colors['Bottom'][8] = \
                self.face_colors['Bottom'][6], self.face_colors['Bottom'][3], self.face_colors['Bottom'][0], \
                    self.face_colors['Bottom'][7], self.face_colors['Bottom'][4], self.face_colors['Bottom'][1], \
                    self.face_colors['Bottom'][8], self.face_colors['Bottom'][5], self.face_colors['Bottom'][2]
        elif move == "di":
            self.apply_move('d')
            self.apply_move('d')
            self.apply_move('d')
        elif move == 'duod' or move == 'duodi':
            self.apply_move('d')
            self.apply_move('d')

        elif move == 'F':
            temp_right = [self.face_colors['Right'][0], self.face_colors['Right'][3], self.face_colors['Right'][6]]
            temp_top = [self.face_colors['Top'][6], self.face_colors['Top'][7], self.face_colors['Top'][8]]
            temp_bottom = [self.face_colors['Bottom'][0], self.face_colors['Bottom'][1], self.face_colors['Bottom'][2]]
            temp_left = [self.face_colors['Left'][2], self.face_colors['Left'][5], self.face_colors['Left'][8]]

            self.face_colors['Right'][0], self.face_colors['Right'][3], self.face_colors['Right'][6] = temp_top
            self.face_colors['Top'][6], self.face_colors['Top'][7], self.face_colors['Top'][8] = temp_left[::-1]
            self.face_colors['Left'][2], self.face_colors['Left'][5], self.face_colors['Left'][8] = temp_bottom
            self.face_colors['Bottom'][0], self.face_colors['Bottom'][1], self.face_colors['Bottom'][2] = temp_right[
                                                                                                          ::-1]

            # # Rotation de la face droite dans le sens horaire
            self.face_colors['Front'][0], self.face_colors['Front'][1], self.face_colors['Front'][2], \
                self.face_colors['Front'][3], self.face_colors['Front'][4], self.face_colors['Front'][5], \
                self.face_colors['Front'][6], self.face_colors['Front'][7], self.face_colors['Front'][8] = \
                self.face_colors['Front'][6], self.face_colors['Front'][3], self.face_colors['Front'][0], \
                    self.face_colors['Front'][7], self.face_colors['Front'][4], self.face_colors['Front'][1], \
                    self.face_colors['Front'][8], self.face_colors['Front'][5], self.face_colors['Front'][2]
        elif move == "Fi":
            self.apply_move('F')
            self.apply_move('F')
            self.apply_move('F')
        elif move == 'duoF' or move == 'duoFi':
            self.apply_move('F')
            self.apply_move('F')

        elif move == 'f':
            temp_right = [self.face_colors['Right'][0], self.face_colors['Right'][3], self.face_colors['Right'][6]]
            temp_top = [self.face_colors['Top'][6], self.face_colors['Top'][7], self.face_colors['Top'][8]]
            temp_bottom = [self.face_colors['Bottom'][0], self.face_colors['Bottom'][1], self.face_colors['Bottom'][2]]
            temp_left = [self.face_colors['Left'][2], self.face_colors['Left'][5], self.face_colors['Left'][8]]
            temp_right_2 = [self.face_colors['Right'][1], self.face_colors['Right'][4], self.face_colors['Right'][7]]
            temp_top_2 = [self.face_colors['Top'][3], self.face_colors['Top'][4], self.face_colors['Top'][5]]
            temp_bottom_2 = [self.face_colors['Bottom'][3], self.face_colors['Bottom'][4],
                             self.face_colors['Bottom'][5]]
            temp_left_2 = [self.face_colors['Left'][1], self.face_colors['Left'][4], self.face_colors['Left'][7]]

            self.face_colors['Right'][0], self.face_colors['Right'][3], self.face_colors['Right'][6] = temp_top
            self.face_colors['Top'][6], self.face_colors['Top'][7], self.face_colors['Top'][8] = temp_left[::-1]
            self.face_colors['Left'][2], self.face_colors['Left'][5], self.face_colors['Left'][8] = temp_bottom
            self.face_colors['Bottom'][0], self.face_colors['Bottom'][1], self.face_colors['Bottom'][2] = temp_right[
                                                                                                          ::-1]
            self.face_colors['Right'][1], self.face_colors['Right'][4], self.face_colors['Right'][7] = temp_top_2
            self.face_colors['Top'][3], self.face_colors['Top'][4], self.face_colors['Top'][5] = temp_left_2[::-1]
            self.face_colors['Bottom'][3], self.face_colors['Bottom'][4], self.face_colors['Bottom'][5] = temp_right_2[
                                                                                                          ::-1]
            self.face_colors['Left'][1], self.face_colors['Left'][4], self.face_colors['Left'][7] = temp_bottom_2

            # # Rotation de la face droite dans le sens horaire
            self.face_colors['Front'][0], self.face_colors['Front'][1], self.face_colors['Front'][2], \
                self.face_colors['Front'][3], self.face_colors['Front'][4], self.face_colors['Front'][5], \
                self.face_colors['Front'][6], self.face_colors['Front'][7], self.face_colors['Front'][8] = \
                self.face_colors['Front'][6], self.face_colors['Front'][3], self.face_colors['Front'][0], \
                    self.face_colors['Front'][7], self.face_colors['Front'][4], self.face_colors['Front'][1], \
                    self.face_colors['Front'][8], self.face_colors['Front'][5], self.face_colors['Front'][2]
        elif move == "fi":
            self.apply_move('f')
            self.apply_move('f')
            self.apply_move('f')
        elif move == 'duof' or move == 'duofi':
            self.apply_move('f')
            self.apply_move('f')

        elif move == 'B':
            temp_right = [self.face_colors['Right'][2], self.face_colors['Right'][5], self.face_colors['Right'][8]]
            temp_top = [self.face_colors['Top'][0], self.face_colors['Top'][1], self.face_colors['Top'][2]]
            temp_bottom = [self.face_colors['Bottom'][6], self.face_colors['Bottom'][7], self.face_colors['Bottom'][8]]
            temp_left = [self.face_colors['Left'][0], self.face_colors['Left'][3], self.face_colors['Left'][6]]

            self.face_colors['Right'][2], self.face_colors['Right'][5], self.face_colors['Right'][8] = temp_bottom[::-1]
            self.face_colors['Top'][0], self.face_colors['Top'][1], self.face_colors['Top'][2] = temp_right
            self.face_colors['Left'][0], self.face_colors['Left'][3], self.face_colors['Left'][6] = temp_top[::-1]
            self.face_colors['Bottom'][6], self.face_colors['Bottom'][7], self.face_colors['Bottom'][8] = temp_left

            # # Rotation de la face droite dans le sens horaire
            self.face_colors['Back'][0], self.face_colors['Back'][1], self.face_colors['Back'][2], \
                self.face_colors['Back'][3], self.face_colors['Back'][4], self.face_colors['Back'][5], \
                self.face_colors['Back'][6], self.face_colors['Back'][7], self.face_colors['Back'][8] = \
                self.face_colors['Back'][6], self.face_colors['Back'][3], self.face_colors['Back'][0], \
                    self.face_colors['Back'][7], self.face_colors['Back'][4], self.face_colors['Back'][1], \
                    self.face_colors['Back'][8], self.face_colors['Back'][5], self.face_colors['Back'][2]
        elif move == "Bi":
            self.apply_move('B')
            self.apply_move('B')
            self.apply_move('B')
        elif move == 'duoB' or move == 'duoBi':
            self.apply_move('B')
            self.apply_move('B')

        elif move == 'b':
            temp_right = [self.face_colors['Right'][2], self.face_colors['Right'][5], self.face_colors['Right'][8]]
            temp_top = [self.face_colors['Top'][0], self.face_colors['Top'][1], self.face_colors['Top'][2]]
            temp_bottom = [self.face_colors['Bottom'][6], self.face_colors['Bottom'][7], self.face_colors['Bottom'][8]]
            temp_left = [self.face_colors['Left'][0], self.face_colors['Left'][3], self.face_colors['Left'][6]]
            temp_right_2 = [self.face_colors['Right'][1], self.face_colors['Right'][4], self.face_colors['Right'][7]]
            temp_top_2 = [self.face_colors['Top'][3], self.face_colors['Top'][4], self.face_colors['Top'][5]]
            temp_bottom_2 = [self.face_colors['Bottom'][3], self.face_colors['Bottom'][4],
                             self.face_colors['Bottom'][5]]
            temp_left_2 = [self.face_colors['Left'][1], self.face_colors['Left'][4], self.face_colors['Left'][7]]

            self.face_colors['Right'][2], self.face_colors['Right'][5], self.face_colors['Right'][8] = temp_bottom[::-1]
            self.face_colors['Top'][0], self.face_colors['Top'][1], self.face_colors['Top'][2] = temp_right
            self.face_colors['Left'][0], self.face_colors['Left'][3], self.face_colors['Left'][6] = temp_top[::-1]
            self.face_colors['Bottom'][6], self.face_colors['Bottom'][7], self.face_colors['Bottom'][8] = temp_left
            self.face_colors['Right'][1], self.face_colors['Right'][4], self.face_colors['Right'][7] = temp_bottom_2[
                                                                                                       ::-1]
            self.face_colors['Top'][3], self.face_colors['Top'][4], self.face_colors['Top'][5] = temp_right_2
            self.face_colors['Bottom'][3], self.face_colors['Bottom'][4], self.face_colors['Bottom'][5] = temp_left_2
            self.face_colors['Left'][1], self.face_colors['Left'][4], self.face_colors['Left'][7] = temp_top_2[::-1]

            # # Rotation de la face droite dans le sens horaire
            self.face_colors['Back'][0], self.face_colors['Back'][1], self.face_colors['Back'][2], \
                self.face_colors['Back'][3], self.face_colors['Back'][4], self.face_colors['Back'][5], \
                self.face_colors['Back'][6], self.face_colors['Back'][7], self.face_colors['Back'][8] = \
                self.face_colors['Back'][6], self.face_colors['Back'][3], self.face_colors['Back'][0], \
                    self.face_colors['Back'][7], self.face_colors['Back'][4], self.face_colors['Back'][1], \
                    self.face_colors['Back'][8], self.face_colors['Back'][5], self.face_colors['Back'][2]
        elif move == "bi":
            self.apply_move('b')
            self.apply_move('b')
            self.apply_move('b')
        elif move == 'duob' or move == 'duobi':
            self.apply_move('b')
            self.apply_move('b')

        elif move == 'M':
            # Implémentez la logique pour le mouvement M (rotation du cube dans le sens de la colonne centrale droite)
            temp_top = [self.face_colors['Top'][1], self.face_colors['Top'][4], self.face_colors['Top'][7]]
            temp_front = [self.face_colors['Front'][1], self.face_colors['Front'][4],
                          self.face_colors['Front'][7]]
            temp_bottom = [self.face_colors['Bottom'][1], self.face_colors['Bottom'][4],
                           self.face_colors['Bottom'][7]]
            temp_back = [self.face_colors['Back'][1], self.face_colors['Back'][4], self.face_colors['Back'][7]]

            self.face_colors['Top'][1], self.face_colors['Top'][4], self.face_colors['Top'][7] = temp_back[::-1]
            self.face_colors['Front'][1], self.face_colors['Front'][4], self.face_colors['Front'][7] = temp_top
            self.face_colors['Bottom'][1], self.face_colors['Bottom'][4], self.face_colors['Bottom'][
                7] = temp_front
            self.face_colors['Back'][1], self.face_colors['Back'][4], self.face_colors['Back'][7] = temp_bottom[::-1]

        elif move == "Mi":
            # Mouvement M inverse (dans le sens antihoraire)
            self.apply_move('M')
            self.apply_move('M')
            self.apply_move('M')
        elif move == 'duoM' or move == 'duoMi':
            self.apply_move('M')
            self.apply_move('M')

        elif move == 'E':
            # Implémentez la logique pour le mouvement E (rotation du cube dans le sens de la ligne centrale du haut)
            temp_front = self.face_colors['Front'][3:6]
            temp_right = self.face_colors['Right'][3:6]
            temp_back = self.face_colors['Back'][3:6]
            temp_left = self.face_colors['Left'][3:6]

            self.face_colors['Front'][3:6] = temp_left
            self.face_colors['Right'][3:6] = temp_front
            self.face_colors['Back'][3:6] = temp_right
            self.face_colors['Left'][3:6] = temp_back

        elif move == "Ei":
            # Mouvement E inverse (dans le sens antihoraire)
            self.apply_move('E')
            self.apply_move('E')
            self.apply_move('E')
        elif move == 'duoE' or move == 'duoEi':
            self.apply_move('E')
            self.apply_move('E')

        elif move == 'S':
            # Implémentez la logique pour le mouvement S (rotation du cube dans le sens de la ligne centrale de droite)
            temp_top = [self.face_colors['Top'][3], self.face_colors['Top'][4], self.face_colors['Top'][5]]
            temp_right = [self.face_colors['Right'][1], self.face_colors['Right'][4],
                          self.face_colors['Right'][7]]
            temp_bottom = [self.face_colors['Bottom'][3], self.face_colors['Bottom'][4],
                           self.face_colors['Bottom'][5]]
            temp_left = [self.face_colors['Left'][1], self.face_colors['Left'][4], self.face_colors['Left'][7]]

            self.face_colors['Top'][3], self.face_colors['Top'][4], self.face_colors['Top'][5] = temp_left[::-1]
            self.face_colors['Right'][1], self.face_colors['Right'][4], self.face_colors['Right'][
                7] = temp_top
            self.face_colors['Bottom'][3], self.face_colors['Bottom'][4], self.face_colors['Bottom'][
                5] = temp_right[::-1]
            self.face_colors['Left'][1], self.face_colors['Left'][4], self.face_colors['Left'][7] = temp_bottom

        elif move == "Si":
            # Mouvement S inverse (dans le sens antihoraire)
            self.apply_move('S')
            self.apply_move('S')
            self.apply_move('S')
        elif move == 'duoS' or move == 'duoSi':
            self.apply_move('S')
            self.apply_move('S')

        elif move == 'X':
            temp_top = [self.face_colors['Top'][0], self.face_colors['Top'][1], self.face_colors['Top'][2],
                        self.face_colors['Top'][3], self.face_colors['Top'][4], self.face_colors['Top'][5],
                        self.face_colors['Top'][6], self.face_colors['Top'][7], self.face_colors['Top'][8]]
            temp_front = [self.face_colors['Front'][0], self.face_colors['Front'][1], self.face_colors['Front'][2],
                          self.face_colors['Front'][3], self.face_colors['Front'][4], self.face_colors['Front'][5],
                          self.face_colors['Front'][6], self.face_colors['Front'][7], self.face_colors['Front'][8]]
            temp_bottom = [self.face_colors['Bottom'][0], self.face_colors['Bottom'][1], self.face_colors['Bottom'][2],
                           self.face_colors['Bottom'][3], self.face_colors['Bottom'][4], self.face_colors['Bottom'][5],
                           self.face_colors['Bottom'][6], self.face_colors['Bottom'][7], self.face_colors['Bottom'][8]]
            temp_back = [self.face_colors['Back'][0], self.face_colors['Back'][1], self.face_colors['Back'][2],
                         self.face_colors['Back'][3], self.face_colors['Back'][4], self.face_colors['Back'][5],
                         self.face_colors['Back'][6], self.face_colors['Back'][7], self.face_colors['Back'][8]]

            self.face_colors['Top'][0], self.face_colors['Top'][1], self.face_colors['Top'][2], self.face_colors['Top'][
                3], self.face_colors['Top'][4], self.face_colors['Top'][5], self.face_colors['Top'][6], \
            self.face_colors['Top'][7], self.face_colors['Top'][8] = temp_front
            self.face_colors['Front'][0], self.face_colors['Front'][1], self.face_colors['Front'][2], \
            self.face_colors['Front'][3], self.face_colors['Front'][4], self.face_colors['Front'][5], \
            self.face_colors['Front'][6], self.face_colors['Front'][7], self.face_colors['Front'][8] = temp_bottom
            self.face_colors['Bottom'][0], self.face_colors['Bottom'][1], self.face_colors['Bottom'][2], \
            self.face_colors['Bottom'][3], self.face_colors['Bottom'][4], self.face_colors['Bottom'][5], \
            self.face_colors['Bottom'][6], self.face_colors['Bottom'][7], self.face_colors['Bottom'][8] = temp_back[
                                                                                                          ::-1]
            self.face_colors['Back'][0], self.face_colors['Back'][1], self.face_colors['Back'][2], \
            self.face_colors['Back'][3], self.face_colors['Back'][4], self.face_colors['Back'][5], \
            self.face_colors['Back'][6], self.face_colors['Back'][7], self.face_colors['Back'][8] = temp_top[::-1]

            self.face_colors['Right'][0], self.face_colors['Right'][1], self.face_colors['Right'][2], \
            self.face_colors['Right'][3], self.face_colors['Right'][4], self.face_colors['Right'][5], \
            self.face_colors['Right'][6], self.face_colors['Right'][7], self.face_colors['Right'][8] = \
            self.face_colors['Right'][6], self.face_colors['Right'][3], self.face_colors['Right'][0], \
            self.face_colors['Right'][7], self.face_colors['Right'][4], self.face_colors['Right'][1], \
            self.face_colors['Right'][8], self.face_colors['Right'][5], self.face_colors['Right'][2]

            self.face_colors['Left'][0], self.face_colors['Left'][1], self.face_colors['Left'][2], \
            self.face_colors['Left'][3], self.face_colors['Left'][4], self.face_colors['Left'][5], \
            self.face_colors['Left'][6], self.face_colors['Left'][7], self.face_colors['Left'][8] = \
            self.face_colors['Left'][2], self.face_colors['Left'][5], self.face_colors['Left'][8], \
            self.face_colors['Left'][1], self.face_colors['Left'][4], self.face_colors['Left'][7], \
            self.face_colors['Left'][0], self.face_colors['Left'][3], self.face_colors['Left'][6]

        elif move == 'Xi':
            self.apply_move('X')
            self.apply_move('X')
            self.apply_move('X')

        elif move == 'duoX' or move == 'duoXi':
            self.apply_move('X')
            self.apply_move('X')

        elif move == 'Z':
            temp_top = [self.face_colors['Top'][0], self.face_colors['Top'][1], self.face_colors['Top'][2],
                        self.face_colors['Top'][3], self.face_colors['Top'][4], self.face_colors['Top'][5],
                        self.face_colors['Top'][6], self.face_colors['Top'][7], self.face_colors['Top'][8]]
            temp_right = [self.face_colors['Right'][0], self.face_colors['Right'][1], self.face_colors['Right'][2],
                          self.face_colors['Right'][3], self.face_colors['Right'][4], self.face_colors['Right'][5],
                          self.face_colors['Right'][6], self.face_colors['Right'][7], self.face_colors['Right'][8]]
            temp_bottom = [self.face_colors['Bottom'][0], self.face_colors['Bottom'][1], self.face_colors['Bottom'][2],
                           self.face_colors['Bottom'][3], self.face_colors['Bottom'][4], self.face_colors['Bottom'][5],
                           self.face_colors['Bottom'][6], self.face_colors['Bottom'][7], self.face_colors['Bottom'][8]]
            temp_left = [self.face_colors['Left'][0], self.face_colors['Left'][1], self.face_colors['Left'][2],
                         self.face_colors['Left'][3], self.face_colors['Left'][4], self.face_colors['Left'][5],
                         self.face_colors['Left'][6], self.face_colors['Left'][7], self.face_colors['Left'][8]]

            self.face_colors['Top'][2], self.face_colors['Top'][5], self.face_colors['Top'][8], self.face_colors['Top'][
                1], self.face_colors['Top'][4], self.face_colors['Top'][7], self.face_colors['Top'][0], \
                self.face_colors['Top'][3], self.face_colors['Top'][6] = temp_left
            self.face_colors['Right'][2], self.face_colors['Right'][5], self.face_colors['Right'][8], \
                self.face_colors['Right'][1], self.face_colors['Right'][4], self.face_colors['Right'][7], \
                self.face_colors['Right'][0], self.face_colors['Right'][3], self.face_colors['Right'][6] = temp_top
            self.face_colors['Bottom'][2], self.face_colors['Bottom'][5], self.face_colors['Bottom'][8], \
                self.face_colors['Bottom'][1], self.face_colors['Bottom'][4], self.face_colors['Bottom'][7], \
                self.face_colors['Bottom'][0], self.face_colors['Bottom'][3], self.face_colors['Bottom'][6] = temp_right
            self.face_colors['Left'][2], self.face_colors['Left'][5], self.face_colors['Left'][8], \
                self.face_colors['Left'][1], self.face_colors['Left'][4], self.face_colors['Left'][7], \
                self.face_colors['Left'][0], self.face_colors['Left'][3], self.face_colors['Left'][6] = temp_bottom

            self.face_colors['Front'][0], self.face_colors['Front'][1], self.face_colors['Front'][2], \
                self.face_colors['Front'][3], self.face_colors['Front'][4], self.face_colors['Front'][5], \
                self.face_colors['Front'][6], self.face_colors['Front'][7], self.face_colors['Front'][8] = \
                self.face_colors['Front'][6], self.face_colors['Front'][3], self.face_colors['Front'][0], \
                    self.face_colors['Front'][7], self.face_colors['Front'][4], self.face_colors['Front'][1], \
                    self.face_colors['Front'][8], self.face_colors['Front'][5], self.face_colors['Front'][2]

            self.face_colors['Back'][0], self.face_colors['Back'][1], self.face_colors['Back'][2], \
                self.face_colors['Back'][3], self.face_colors['Back'][4], self.face_colors['Back'][5], \
                self.face_colors['Back'][6], self.face_colors['Back'][7], self.face_colors['Back'][8] = \
                self.face_colors['Back'][2], self.face_colors['Back'][5], self.face_colors['Back'][8], \
                    self.face_colors['Back'][1], self.face_colors['Back'][4], self.face_colors['Back'][7], \
                    self.face_colors['Back'][0], self.face_colors['Back'][3], self.face_colors['Back'][6]

        elif move == 'Zi':
            self.apply_move('Z')
            self.apply_move('Z')
            self.apply_move('Z')

        elif move == 'duoZ' or move == 'duoZi':
            self.apply_move('Z')
            self.apply_move('Z')

        elif move == 'Y':

            temp_front = [self.face_colors['Front'][0], self.face_colors['Front'][1], self.face_colors['Front'][2],
                          self.face_colors['Front'][3], self.face_colors['Front'][4], self.face_colors['Front'][5],
                          self.face_colors['Front'][6], self.face_colors['Front'][7], self.face_colors['Front'][8]]
            temp_right = [self.face_colors['Right'][0], self.face_colors['Right'][1], self.face_colors['Right'][2],
                          self.face_colors['Right'][3], self.face_colors['Right'][4], self.face_colors['Right'][5],
                          self.face_colors['Right'][6], self.face_colors['Right'][7], self.face_colors['Right'][8]]
            temp_back = [self.face_colors['Back'][0], self.face_colors['Back'][1], self.face_colors['Back'][2],
                         self.face_colors['Back'][3], self.face_colors['Back'][4], self.face_colors['Back'][5],
                         self.face_colors['Back'][6], self.face_colors['Back'][7], self.face_colors['Back'][8]]
            temp_left = [self.face_colors['Left'][0], self.face_colors['Left'][1], self.face_colors['Left'][2],
                         self.face_colors['Left'][3], self.face_colors['Left'][4], self.face_colors['Left'][5],
                         self.face_colors['Left'][6], self.face_colors['Left'][7], self.face_colors['Left'][8]]

            self.face_colors['Front'][0], self.face_colors['Front'][1], self.face_colors['Front'][2], \
                self.face_colors['Front'][3], self.face_colors['Front'][4], self.face_colors['Front'][5], \
                self.face_colors['Front'][6], self.face_colors['Front'][7], self.face_colors['Front'][8] = temp_right
            self.face_colors['Right'][0], self.face_colors['Right'][1], self.face_colors['Right'][2], \
                self.face_colors['Right'][3], self.face_colors['Right'][4], self.face_colors['Right'][5], \
                self.face_colors['Right'][6], self.face_colors['Right'][7], self.face_colors['Right'][8] = temp_back
            self.face_colors['Back'][0], self.face_colors['Back'][1], self.face_colors['Back'][2], \
                self.face_colors['Back'][3], self.face_colors['Back'][4], self.face_colors['Back'][5], \
                self.face_colors['Back'][6], self.face_colors['Back'][7], self.face_colors['Back'][8] = temp_left
            self.face_colors['Left'][0], self.face_colors['Left'][1], self.face_colors['Left'][2], \
                self.face_colors['Left'][3], self.face_colors['Left'][4], self.face_colors['Left'][5], \
                self.face_colors['Left'][6], self.face_colors['Left'][7], self.face_colors['Left'][8] = temp_front

            self.face_colors['Top'][0], self.face_colors['Top'][1], self.face_colors['Top'][2], self.face_colors['Top'][
                3], self.face_colors['Top'][4], self.face_colors['Top'][5], self.face_colors['Top'][6], \
                self.face_colors['Top'][7], self.face_colors['Top'][8] = self.face_colors['Top'][6], \
                self.face_colors['Top'][3], self.face_colors['Top'][0], self.face_colors['Top'][7], \
            self.face_colors['Top'][
                4], self.face_colors['Top'][1], self.face_colors['Top'][8], self.face_colors['Top'][5], \
                self.face_colors['Top'][2]

            self.face_colors['Bottom'][0], self.face_colors['Bottom'][1], self.face_colors['Bottom'][2], \
                self.face_colors['Bottom'][3], self.face_colors['Bottom'][4], self.face_colors['Bottom'][5], \
                self.face_colors['Bottom'][6], self.face_colors['Bottom'][7], self.face_colors['Bottom'][8] = \
                self.face_colors['Bottom'][2], self.face_colors['Bottom'][5], self.face_colors['Bottom'][8], \
                    self.face_colors['Bottom'][1], self.face_colors['Bottom'][4], self.face_colors['Bottom'][7], \
                    self.face_colors['Bottom'][0], self.face_colors['Bottom'][3], self.face_colors['Bottom'][6]

        elif move == 'Yi':
            self.apply_move('Y')
            self.apply_move('Y')
            self.apply_move('Y')

        elif move == 'duoY' or move == 'duoYi':
            self.apply_move('Y')
            self.apply_move('Y')

        else:
            print("Mouvement non reconnu")

        # print("Move applied successfully")
        return True

    def play_audio_file(self):
        self.audio_timer.stop()
        self.update_face_colors(self.face_colors)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("Happy_Victory_Song.mp3")
        pygame.mixer.music.play(start=55)
        pygame.mixer.music.play(stop=65)

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

# if __name__ == '__main__':
# # Initialize face colors to all white
# initial_face_colors = {
#     "Back": ['red'] * 9,
#     "Left": ['green'] * 9,
#     "Top": ['yellow'] * 9,
#     "Right": ['blue'] * 9,
#     "Front": ['orange'] * 9,
#     "Top": ['white'] * 9
# }
#
# app = QApplication(sys.argv)
# cube_display = CubeDisplay(initial_face_colors)
# cube_display.show()
#
# sys.exit(app.exec_())
