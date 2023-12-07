
import bluetooth
import datetime
from datetime import datetime

import uuid
import time
 
class bl:
    def __init__(self):
        print (':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
        for ele in range(0,8*6,8)][::-1]))

        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        port = 1
        self.server_socket.bind(("", port))

        self.server_socket.listen(1)

        print("waiting for connection...")

        self.client_socket, addr = self.server_socket.accept()
        print("connection from", addr)
    
    def loop(self, data):
        while True:
            try:
                now = datetime.now()
                d = now.strftime("%m/%d/%Y")
                t = now.strftime("%H:%M:%S")
                csv_str = ""
                csv_str = ",".join([d])
                csv_str = ",".join([csv_str, t])
                csv_str = ",".join([csv_str, str(data["sat_count"])])
                csv_str = ",".join([csv_str, str(data["lat"])])
                csv_str = ",".join([csv_str, str(data["long"])])
                csv_str = ",".join([csv_str, str(data["ele"])])
                csv_str = ",".join([csv_str, str(data["acc"][0])])
                csv_str = ",".join([csv_str, str(data["acc"][1])])
                csv_str = ",".join([csv_str, str(data["acc"][2])])

                csv_str = ",".join([csv_str, str(data["mag"][0])])
                csv_str = ",".join([csv_str, str(data["mag"][1])])
                csv_str = ",".join([csv_str, str(data["mag"][2])])

                csv_str = ",".join([csv_str, str(data["vel"][0])])
                csv_str = ",".join([csv_str, str(data["vel"][1])])
                csv_str = ",".join([csv_str, str(data["vel"][2])])
                self.client_socket.send((csv_str+"\n\n").encode("utf-8"))
                time.sleep(1)

            except Exception as e:
                print("Error", e)
                break

        self.client_socket.close()
        self.server_socket.close()

