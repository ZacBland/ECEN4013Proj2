
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from .imu import IMU

import serial
import sys
import glob
from serial.tools.list_ports import comports
from time import sleep
from .gps import GPS


ser = None
class Context(QMainWindow):

    def __init__(self):
        super().__init__()
        self.central_widget = QWidget()
        self.central_widget.setFocus()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setStyleSheet(''' font-size: 24px; ''')
        self.setMinimumSize(200,200)
        self.display_btn = QPushButton("Start Display")
        self.start = True
        self.display_btn.setFlat(False)
        self.display_btn.setFixedHeight(50)
        self.display_btn.pressed.connect(self.start_display)
        self.display_btn.setStyleSheet("background-color : green") 
        self.main_layout.addWidget(self.display_btn)

        self.gps = GPS()
        self.gps.setVisible(False)
        self.main_layout.addWidget(self.gps)

        self.imu = IMU()
        self.imu.setVisible(False)
        self.main_layout.addWidget(self.imu)

        self.thread = QThread()
        self.worker = Worker()
        self.worker.moveToThread(self.thread)

        self.worker.update_gps.connect(self.update)

        self.thread.started.connect(self.worker.do_work)
        self.thread.start()

    def start_display(self):
        if self.start:
            self.start = False
            self.gps.setVisible(True)
            self.imu.setVisible(True)
            self.display_btn.setStyleSheet("background-color : red") 
            self.display_btn.setText("End Display")
            self.adjustSize()
            self.worker.restart()

        else:
            self.start = True
            self.gps.setVisible(False)
            self.imu.setVisible(False)
            self.display_btn.setStyleSheet("background-color : green") 
            self.display_btn.setText("Start Display")
            self.adjustSize()
            self.worker.stop()
    
    


    def update(self, gui_dict):        
        self.gps.update(gui_dict)
        self.imu.update(gui_dict)

class Worker(QObject):
    update_gps = pyqtSignal(dict)  # give worker class a finished signal

    def __init__(self, parent=None):
        QObject.__init__(self, parent=parent)
        self.running = False
        #self.parent = parent

    def do_work(self):
        
        print("Connecting...")
        print(get_port()[0])
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
            "vel": (0.0,0.0,0.0),
            "ori": (0.0,0.0,0.0)
        }

        while True:
            try:
                while not self.running:
                    pass
                received_data = ser.read()
                sleep(0.03)
                data_left = ser.inWaiting() 
                received_data += ser.read(data_left)
                received_data = received_data.decode("utf-8")


                
                
                info = received_data.split(',')
                if info[4] == "gps":
                    gui_dict["sat_count"] = info[5]
                    gui_dict["lat"] = info[6]
                    gui_dict["long"] = info[7]
                    gui_dict["ele"] = info[8]
                elif info[4] == "acc":
                    if(info[5] != 'None'):
                        gui_dict["acc"] = (info[5],info[6],info[7])
                elif info[4] == "mag":
                    if(info[5] != 'None'):
                        gui_dict["mag"] = (info[5],info[6],info[7])
                elif info[4] == "vel":
                    if(info[5] != 'None'):
                        gui_dict["vel"] = (info[5],info[6],info[7])
                elif info[0] == "ori":
                    gui_dict["ori"] = (info[1],info[2],info[3])
                

                self.update_gps.emit(gui_dict)

            except Exception as e:
                print("Error:",e)
    
    def stop(self):
        self.running = False

    def restart(self):
        self.running = True

        
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

