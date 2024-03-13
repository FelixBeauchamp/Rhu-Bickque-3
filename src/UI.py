import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTabWidget, QTextEdit
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QPen, QColor

app = QtWidgets.QApplication(sys.argv)
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowTitle('Algo_Ass')
        self.setGeometry(700, 200, 600, 600)  # x, y, width, height

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Contrôle")
        self.tabs.addTab(self.tab2, "Vue de la face")

        # Create first tab
        self.pushButton1 = QPushButton("PyQt5 button", self.tab1)
        self.pushButton1.setText('Start')
        self.pushButton1.setGeometry(200, 100, 150, 30)
        self.pushButton1.clicked.connect(self.__b1__)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.gros_carre = faceDuCube(self.tab2)
        self.gros_carre.setGeometry(100, 100, 400, 300)
    def __b1__(self):
        print('test')
class faceDuCube(QWidget):

    def whatsdacolor(color):
        if color == "Y":
            return [255,255,0]
        elif color == "B":
            return [0,0,255]
        elif color == "R":
            return [255,0,0]
        elif color == "O":
            return [255,125,0]
        elif color == "W":
            return [255,255,255]
        elif color == "G":
            return [0,255,0]
    def paintEvent(self, event):
        painter = QPainter(self)
        test_couleur = ["Y","B","G","Y","Y","R","W","B","O"]
        origine_carre = 20
        taille_carre = 50
        space = 10

        for i in range(3):
            for j in range(3):
                painter.setPen(QColor(0, 0, 0))
                actual_color = test_couleur[(i-1)*3+j]
                rgb_values = [255,255,255]
                #rgb_values = self.whatsdacolor(actual_color)
                painter.setBrush(QColor(rgb_values[0],rgb_values[1],rgb_values[2]))
                painter.drawRect(origine_carre+i*taille_carre+i*space, origine_carre+j*taille_carre+j*space, taille_carre, taille_carre)  # x, y, width, height

main_window = MyWindow()
main_window.show()

sys.exit(app.exec())