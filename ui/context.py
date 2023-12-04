
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5 import QtCore
from .imu import IMU
from .recieve import UART

import serial
import sys
import glob
from serial.tools.list_ports import comports
from time import sleep
import json
from .gps import GPS


ser = None
class Context(QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.central_widget.setFocus()
        self.setCentralWidget(self.central_widget)

        self.setMinimumSize(400,400)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setAlignment(QtCore.Qt.AlignCenter)

        self.gps = GPS()
        main_layout.addWidget(self.gps)

        self.imu = IMU()
        main_layout.addWidget(self.imu)

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.worker.update_gps.connect(self.update)

        self.thread.started.connect(self.worker.do_work)
        self.thread.start()
        self.test = None


    def update(self, gui_dict):        
        self.gps.update(gui_dict)
        self.imu.update(gui_dict)

class Worker(QObject):
    update_gps = pyqtSignal(dict)  # give worker class a finished signal

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        #self.parent = parent

    def do_work(self):
        
        print("Connecting...")
        ser = None
        while ser is None:
            try:
                ser = serial.Serial(get_port()[0], timeout=5)
            except Exception as e:
                print("Failed Connection, trying again...")
                QThread.sleep(1)
        print("Connected to Pi.")

        gui_dict = {
            "sat_count":0,
            "lat": 0.0,
            "long": 0.0,
            "ele": 0.0,
            "acc": (0.0,0.0,0.0),
            "mag": (0.0,0.0,0.0),
            "vel": (0.0,0.0,0.0)
        }

        all_zeros = True
        while True:
            received_data = ser.read()
            sleep(0.03)
            data_left = ser.inWaiting() 
            received_data += ser.read(data_left)
            received_data = received_data.decode("utf-8")

            info = received_data.split(',')
            if info[0] == "gps":
                gui_dict["sat_count"] = info[1]
                gui_dict["lat"] = info[2]
                gui_dict["long"] = info[3]
                gui_dict["ele"] = info[4]
            elif info[0] == "acc":
                gui_dict["acc"] = (info[1],info[2],info[3])
            elif info[0] == "mag":
                gui_dict["mag"] = (info[1],info[2],info[3])
            elif info[0] == "vel":
                gui_dict["vel"] = (info[1],info[2],info[3])

            if not all_zeros:
                self.update_gps.emit(gui_dict)
            else:
                if gui_dict["lat"] != 0.0:
                    all_zeros = False
    

        
def get_port():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

