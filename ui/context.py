
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.Qt import *
from .gps import GPS
from .imu import IMU

class Context(QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.central_widget.setFocus()
        self.setCentralWidget(self.central_widget)

        self.setMinimumSize(400,400)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setAlignment(Qt.AlignCenter)

        self.gps = GPS()
        main_layout.addWidget(self.gps)

        self.imu = IMU()
        main_layout.addWidget(self.imu)

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.worker.update.connect(self.update)

        self.thread.started.connect(self.worker.do_work)
        self.thread.start()


    def update(self):
        import random
        data = { #FAKE DATA
            "sat_count": random.randrange(0, 3, 1),
            "lat": random.uniform(-90, 90),
            "long": random.uniform(-180, 180),
            "ele": random.uniform(0, 10000),
            "acc": (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)),
            "mag": (random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(-100, 100)),
            "vel": (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
        }

        self.gps.update(data)
        self.imu.update(data)


class Worker(QObject):
    update = pyqtSignal()  # give worker class a finished signal

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)

    def do_work(self):
        while 1:  # give the loop a stoppable condition

            QThread.sleep(1)
            self.update.emit()


