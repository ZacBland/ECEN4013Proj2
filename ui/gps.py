from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout
from PyQt5.QtGui import *
from PyQt5 import QtCore

class GPS(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("GPS"), alignment=QtCore.Qt.AlignCenter)

        self.grid = QGridLayout()
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: green;')

        self.grid.addWidget(QLabel("Satellites:"), 0, 0, alignment=QtCore.Qt.AlignRight)
        self.grid.addWidget(QLabel("Latitude:"), 1, 0, alignment=QtCore.Qt.AlignRight)
        self.grid.addWidget(QLabel("Longitude:"), 2, 0, alignment=QtCore.Qt.AlignRight)
        self.grid.addWidget(QLabel("Elevation (M):"), 3, 0, alignment=QtCore.Qt.AlignRight)

        self.sat_label = QLabel("Looking for Satellites...")
        self.lat_label = QLabel("-")
        self.long_label = QLabel("-")
        self.ele_label = QLabel("-")

        self.grid.addWidget(self.sat_label, 0, 1)
        self.grid.addWidget(self.lat_label, 1, 1)
        self.grid.addWidget(self.long_label, 2, 1)
        self.grid.addWidget(self.ele_label, 3, 1)

        self.layout.addLayout(self.grid)

        self.setLayout(self.layout)

    def update(self, data: dict):
        self.sat_label.setText(str(data["sat_count"]))
        self.lat_label.setText(str(data["lat"]))
        self.long_label.setText(str(data["long"]))
        self.ele_label.setText(str(data["ele"]))
