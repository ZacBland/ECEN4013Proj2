from uart import UART
from threading import Thread
from time import sleep
import random

data = {
    "sat_count": 0,
    "lat": 0.0,
    "long": 0.0,
    "ele": 0.0,
    "acc": (0.0, 0.0, 0.0),
    "mag": (0.0, 0.0, 0.0),
    "vel": (0.0, 0.0, 0.0)
}


if __name__ == "__main__":

    ser = UART()
    uart_thread = Thread(target=ser.loop, args=(data, ))
    uart_thread.start()

    while(True):
        data["sat_count"] = random.randrange(0, 3, 1)
        data["lat"] = random.uniform(-90, 90)
        data["long"] = random.uniform(-180, 180)
        data["ele"] = random.uniform(0, 10000)
        data["acc"] = (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10))
        data["mag"] = (random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(-100, 100))
        data["vel"] = (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1))
        sleep(1)
    
    

