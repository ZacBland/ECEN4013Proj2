import serial
import json
from time import sleep

BAUD=9600

class UART:
    def __init__(self) -> None:
        self.ser = serial.Serial("/dev/ttyS0", baudrate=9600)
        print("waiting for UART connection...")

        received_data = self.ser.read()
        sleep(0.03)
        data_left = self.ser.inWaiting() 
        received_data += self.ser.read(data_left)
        string = received_data.decode('utf-8')
        print(string)
        if string != "pc_connect\0":
            raise Exception("Error in recieving connection from pi.")
        sleep(0.2)
        self.ser.write("pi_connect\0".encode('utf-8')) 
        sleep(1)
        print("Connected to PC.")

    running = True
    def loop(self, data):
        while self.running:
            self.ser.write(data["sat_count"].encode('utf-8')) 
            sleep(0.1)
            self.ser.write(data["lat"].encode('utf-8')) 
            sleep(0.1)
            self.ser.write(data["long"].encode('utf-8')) 
            sleep(0.1)
            self.ser.write(data["ele"].encode('utf-8')) 
            sleep(0.1)
            self.ser.write(data["acc"].encode('utf-8')) 
            sleep(0.1)
            self.ser.write(data["mag"].encode('utf-8')) 
            sleep(0.1)
            self.ser.write(data["vel"].encode('utf-8')) 
            sleep(0.1)

    def stop(self):
        self.running = False