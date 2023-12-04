import os
import time
import datetime
from datetime import datetime

class SD:
    def __init__(self) -> None:
        self.get_drive()
        time.sleep(2)
    
    def get_drive(self):
        self.drive = None
        error_occurred = False
        while self.drive is None:
            try:
                self.drive = os.listdir("/media/zac/")[0]
            except Exception as e:
                if not error_occurred:
                    print("Drive not found. Please check external SD Card")
                    error_occurred = True
        self.drive = os.path.join("/media/zac/", self.drive)
        print(self.drive)

    def loop(self, data:dict):
        #clear file
        while True:
            try:
                title = ["Date", "Time", "Satellites", "Latitude", "Longitude", "Elevation MSL (m)", "X Accel (m/s^2)",\
                        "Y Accel (m/s^2)","Z Accel (m/s^2)", "X Mag (uT)","Y Mag (uT)","Z Mag (uT)", "X Gyro (rps)", \
                        "Y Gyro (rps)", "Z Gyro (rps)"]
                title_str = ",".join(title)
                with open(os.path.join(self.drive, "file.csv"), "w") as f:
                    f.write(title_str + "\n")

                while True:
                    now = datetime.now()
                    d = now.strftime("%m/%d/%Y")
                    t = now.strftime("%H:%M:%S")
                    csv_str = ""
                    with open(os.path.join(self.drive, "file.csv"), "a") as f:
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
                        
                        f.write(csv_str+ "\n")
                    time.sleep(1)
            except Exception as e:
                self.get_drive()
                time.sleep(2)
