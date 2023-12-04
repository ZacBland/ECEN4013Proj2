from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QVBoxLayout
from PyQt5.QtGui import *
from PyQt5 import QtCore


class IMU(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("IMU"), alignment=QtCore.Qt.AlignCenter)

        self.grid = QGridLayout()
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet('background-color: #8B8000;')

        self.grid.addWidget(QLabel("X Acceleration (m/s^2):"), 0, 0, alignment=QtCore.Qt.AlignRight)
        self.grid.addWidget(QLabel("Y Acceleration (m/s^2):"), 1, 0, alignment=QtCore.Qt.AlignRight)
        self.grid.addWidget(QLabel("Z Acceleration (m/s^2):"), 2, 0, alignment=QtCore.Qt.AlignRight)
        self.grid.addWidget(QLabel(""), 3, 0)

        self.grid.addWidget(QLabel("X Magnetic Field (uT):"), 4, 0, alignment=QtCore.Qt.AlignRight)
        self.grid.addWidget(QLabel("Y Magnetic Field (uT):"), 5, 0, alignment=QtCore.Qt.AlignRight)
        self.grid.addWidget(QLabel("Z Magnetic Field (uT):"), 6, 0, alignment=QtCore.Qt.AlignRight)
        self.grid.addWidget(QLabel(""), 7, 0)

        self.grid.addWidget(QLabel("X Angular Velocity (rps):"), 8, 0, alignment=QtCore.Qt.AlignRight)
        self.grid.addWidget(QLabel("Y Angular Velocity (rps):"), 9, 0, alignment=QtCore.Qt.AlignRight)
        self.grid.addWidget(QLabel("Z Angular Velocity (rps):"), 10, 0, alignment=QtCore.Qt.AlignRight)

        self.x_acc_lab = QLabel("-")
        self.y_acc_lab = QLabel("-")
        self.z_acc_lab = QLabel("-")

        self.x_mag_lab = QLabel("-")
        self.y_mag_lab = QLabel("-")
        self.z_mag_lab = QLabel("-")

        self.x_vel_lab = QLabel("-")
        self.y_vel_lab = QLabel("-")
        self.z_vel_lab = QLabel("-")

        self.grid.addWidget(self.x_acc_lab, 0, 1)
        self.grid.addWidget(self.y_acc_lab, 1, 1)
        self.grid.addWidget(self.z_acc_lab, 2, 1)

        self.grid.addWidget(self.x_mag_lab, 4, 1)
        self.grid.addWidget(self.y_mag_lab, 5, 1)
        self.grid.addWidget(self.z_mag_lab, 6, 1)

        self.grid.addWidget(self.x_vel_lab, 8, 1)
        self.grid.addWidget(self.y_vel_lab, 9, 1)
        self.grid.addWidget(self.z_vel_lab, 10, 1)

        self.layout.addLayout(self.grid)

        self.setLayout(self.layout)

    def update(self, data: dict):
        self.x_acc_lab.setText(str(data["acc"][0]))
        self.y_acc_lab.setText(str(data["acc"][1]))
        self.z_acc_lab.setText(str(data["acc"][2]))

        self.x_mag_lab.setText(str(data["mag"][0]))
        self.y_mag_lab.setText(str(data["mag"][1]))
        self.z_mag_lab.setText(str(data["mag"][2]))

        self.x_vel_lab.setText(str(data["vel"][0]))
        self.y_vel_lab.setText(str(data["vel"][1]))
        self.z_vel_lab.setText(str(data["vel"][2]))

