from uart import UART
from sd import SD
from data import Data
from bl import bl
from threading import Thread
from time import sleep
import random

class Main():
    def __init__(self) -> None:
        self.data = {
            "sat_count": 0,
            "lat": 0.0,
            "long": 0.0,
            "ele": 0.0,
            "acc": (0.0, 0.0, 0.0),
            "mag": (0.0, 0.0, 0.0),
            "vel": (0.0, 0.0, 0.0),
            "ori": (0.0, 0.0, 0.0)
        }

        d = Data(self)
        data_thread = Thread(target=d.loop, args=())
        data_thread.start()
        print("Started GPS/IMU thread")

        ser = UART()
        uart_thread = Thread(target=ser.loop, args=(self.data, ))
        uart_thread.start()
        print("Started UART Thread")

        sd = SD()
        sd_thread = Thread(target=sd.loop, args=(self.data, ))
        sd_thread.start()
        print("Started SD Thread")

        bt = bl()
        bt_thread = Thread(target=bt.loop, args=(self.data, ))
        bt_thread.start()
        print("Started BT Thread")

        
        while(True):
            sleep(1)


Main()    
    

