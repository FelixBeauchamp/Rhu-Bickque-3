import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QProgressBar
from PyQt5.QtCore import QTimer, QTime

class CubeDisplay(QWidget):
    def __init__(self, initial_colors, parent=None):
        super().__init__(parent)
        self.face_colors = initial_colors
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.grid_layout = QGridLayout()
        self.grid_layout.setHorizontalSpacing(50)  # Add horizontal spacing between faces
        self.grid_layout.setVerticalSpacing(50)    # Add vertical spacing between faces
        self.setup_faces()
        layout.addLayout(self.grid_layout)

        # Add apply button
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(self.apply_button)

        # Add timer widgets
        self.timer_label = QLabel("Time elapsed: 0:00.00")
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_timer)
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_timer)
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_timer)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.reset_button)

        # Add spacing between apply button and timer widgets
        layout.addSpacing(20)

        # Add progress bar and percentage label
        self.progress_label = QLabel("Progress: 0%")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 120)  # Set the range of the progress bar
        self.progress_bar.setValue(0)  # Start with the progress bar empty
        layout.addWidget(self.progress_label)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def setup_faces(self):
        # Define the order of the faces for the cross shape
        face_order = [("Back", 0, 1), ("Top", 1, 0), ("Left", 1, 1), ("Right", 1, 2), ("Front", 2, 1), ("Bottom", 3, 1)]
        for i, (face_name, row, col) in enumerate(face_order):
            face_grid = QGridLayout()
            face_grid.setHorizontalSpacing(10)  # Add horizontal spacing between squares
            face_grid.setVerticalSpacing(10)    # Add vertical spacing between squares
            face_colors = self.face_colors[face_name]
            for seg_idx, color in enumerate(face_colors):
                label = QPushButton()
                label.setStyleSheet(f"background-color: {color}; border: 1px solid black;")
                label.setFixedSize(50, 50)
                label.clicked.connect(lambda state, f=face_name, s=seg_idx: self.change_color(f, s))
                face_grid.addWidget(label, seg_idx // 3, seg_idx % 3)
            self.grid_layout.addLayout(face_grid, row, col)

    def change_color(self, face_name, seg_idx):
        color_map = ['white', 'red', 'green', 'yellow', 'blue', 'orange']
        current_color = self.face_colors[face_name][seg_idx]
        next_color = color_map[(color_map.index(current_color) + 1) % len(color_map)]
        self.face_colors[face_name][seg_idx] = next_color
        sender = self.sender()
        sender.setStyleSheet(f"background-color: {next_color}; border: 1px solid black;")

    def apply_changes(self):
        print("Initial face colors array after applying changes:")
        for face_name, colors in self.face_colors.items():
            print(f"{face_name}: {colors}")

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        if hasattr(self, 'elapsed_time'):
            self.start_time = QTime.currentTime().addMSecs(-self.elapsed_time)
        else:
            self.start_time = QTime.currentTime()
        self.timer.start(10)  # Update timer every 10 ms

    def stop_timer(self):
        self.timer.stop()
        self.elapsed_time = self.start_time.elapsed()

    def reset_timer(self):
        self.timer_label.setText("Time elapsed: 0:00.00")
        if hasattr(self, 'timer'):
            self.timer.stop()
            del self.elapsed_time  # Remove elapsed time attribute
        self.progress_bar.setValue(0)  # Reset progress bar value
        self.progress_label.setText("Progress: 0%")

    def update_timer(self):
        current_time = QTime.currentTime()
        elapsed_time = self.start_time.msecsTo(current_time)
        minutes = elapsed_time // 60000
        seconds = (elapsed_time % 60000) // 1000
        milliseconds = elapsed_time % 1000
        self.timer_label.setText(f"Time elapsed: {minutes}:{seconds:02}.{milliseconds:02}")

        # Update progress bar value and percentage label
        self.progress_bar.setValue(seconds)
        progress_percent = (seconds / 120) * 100
        self.progress_label.setText(f"Progress: {progress_percent:.1f}%")


if __name__ == '__main__':
    # Initialize face colors to all white
    initial_face_colors = {
        "Back": ['white'] * 9,
        "Left": ['white'] * 9,
        "Top": ['white'] * 9,
        "Right": ['white'] * 9,
        "Front": ['white'] * 9,
        "Bottom": ['white'] * 9
    }

    app = QApplication(sys.argv)
    cube_display = CubeDisplay(initial_face_colors)
    cube_display.show()
    sys.exit(app.exec_())