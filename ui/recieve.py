import serial
import sys
import glob
from serial.tools.list_ports import comports
from time import sleep
import json

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

class UART:
    def __init__(self):
        print("Connecting...")
        self.ser = serial.Serial(get_port()[0], timeout=5)
        self.ser.write("pc_connect\0".encode('utf-8')) 
        sleep(1)
        received_data = self.ser.read()
        sleep(0.03)
        data_left = self.ser.inWaiting() 
        received_data += self.ser.read(data_left)
        string = received_data.decode('utf-8')
        if string != "pi_connect\0":
            print(string)
            raise Exception("Error in recieving connection from pi.")
        print("Connected to Pi.")
        self.loop()

    def loop(self):
        while(True):
            received_data = self.ser.read()
            sleep(0.03)
            data_left = self.ser.inWaiting() 
            received_data += self.ser.read(data_left)
            print(received_data.decode("utf-8"))



UART()