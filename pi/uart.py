import serial
import json
from time import sleep

BAUD=9600

class UART:
    def __init__(self) -> None:
        self.ser = serial.Serial("/dev/ttyS0", baudrate=9600)

    running = True
    def loop(self, data):
        count = 1
        while self.running:
            gps = ",".join(["ori",str(data["ori"][0]),str(data["ori"][1]),str(data["ori"][2]),"gps",str(data["sat_count"]),str(data["lat"]),str(data["long"]),str(data["ele"])])
            self.ser.write((gps).encode("utf-8")) 
            sleep(0.1)
            acc = ",".join(["ori",str(data["ori"][0]),str(data["ori"][1]),str(data["ori"][2]),"acc",str(data["acc"][0]),str(data["acc"][1]),str(data["acc"][2])])
            self.ser.write((acc).encode("utf-8")) 
            sleep(0.1)
            mag = ",".join(["ori",str(data["ori"][0]),str(data["ori"][1]),str(data["ori"][2]),"mag",str(data["mag"][0]),str(data["mag"][1]),str(data["mag"][2])])
            self.ser.write((mag).encode("utf-8")) 
            sleep(0.1)
            vel = ",".join(["ori",str(data["ori"][0]),str(data["ori"][1]),str(data["ori"][2]),"vel",str(data["vel"][0]),str(data["vel"][1]),str(data["vel"][2])])
            self.ser.write((vel).encode("utf-8")) 
            sleep(0.1)

    def stop(self):
        self.running = False