import busio
import adafruit_bno055
import smbus
import json
import logging 
import time

address = 0x10
gpsReadInterval = 0.1
LOG = logging.getLogger()

GPSDAT = {
    'strType': None,
    'fixTime': None,
    'lat': None,
    'latDir': None,
    'lon': None,
    'lonDir': None,
    'fixQual': None,
    'numSat': None,
    'horDil': None,
    'alt': None,
    'altUnit': None
}

def parseResponse(gpsLine):
    global lastLocation
    gpsChars = ''.join(chr(c) for c in gpsLine)
    if "*" not in gpsChars:
        return False

    gpsStr, chkSum = gpsChars.split('*')    
    gpsComponents = gpsStr.split(',')
    gpsStart = gpsComponents[0]
    if (gpsStart == "$GNGGA"):
        chkVal = 0
        for ch in gpsStr[1:]: # Remove the $
            chkVal ^= ord(ch)
        if (chkVal == int(chkSum, 16)):
            for i, k in enumerate(
                ['strType', 'fixTime', 
                'lat', 'latDir', 'lon', 'lonDir',
                'fixQual', 'numSat', 'horDil', 
                'alt', 'altUnit']):
                GPSDAT[k] = gpsComponents[i]

class Data():

    def __init__(self, parent) -> None:
        self.parent = parent
        self.gps = None
        self.imu = None

        try:
            self.connectGPS()
        except Exception as e:
            print("Unable to connect GPS through I2C.")
        else:
            print("Connected GPS.")

        try:
            mag_i2c = busio.I2C(1,0)
            self.imu = adafruit_bno055.BNO055_I2C(mag_i2c)
        except Exception as e:
            print("Unable to connect IMU through I2C.")
        else:
            print("Connected IMU.")

    def connectGPS(self):
        self.gps = smbus.SMBus(1)

    def loop(self):
        while True:
            try:
                self.readGPS()
                getattr(self.parent, "data")["sat_count"] = GPSDAT['numSat']
                if type(GPSDAT["lat"]) is str:
                    lat = GPSDAT['lat'][:2] +"."+ GPSDAT['lat'][2:4] + GPSDAT['lat'][5:]
                    if(GPSDAT['latDir'] == "s"):
                        lat = "-" + lat
                    getattr(self.parent, "data")["lat"] = lat
                if type(GPSDAT["lat"]) is str:
                    long = GPSDAT['lon'][1:3] +"."+ GPSDAT['lon'][3:5] + GPSDAT['lon'][6:]
                    if(GPSDAT['lonDir'] == "W"):
                        long = "-" + long
                    getattr(self.parent, "data")["long"] = long

                getattr(self.parent, "data")["ele"] = GPSDAT['alt']

                getattr(self.parent, "data")["mag"] = (round(self.imu.magnetic[0],3),round(self.imu.magnetic[1],3),round(self.imu.magnetic[2],3))
                getattr(self.parent, "data")["acc"] = (round(self.imu.acceleration[0],3),round(self.imu.acceleration[1],3),round(self.imu.acceleration[2],3))
                getattr(self.parent, "data")["vel"] = (round(self.imu.gyro[0],3),round(self.imu.gyro[1],3),round(self.imu.gyro[2],3))
                getattr(self.parent, "data")["ori"] = self.imu.euler

            except Exception as e:
                pass
            time.sleep(gpsReadInterval)


    def readGPS(self):
        c = None
        response = []
        try:
            while True: # Newline, or bad char.
                c = self.gps.read_byte(address)
                if c == 255:
                    return False
                elif c == 10:
                    break
                else:
                    response.append(c)
            parseResponse(response)
        except IOError:
            self.connectBus()
        except Exception as e:
            print(e)
            LOG.error(e)

    def readIMU(self):
        return self.imu.magnetic
    
        

