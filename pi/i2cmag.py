import time
import board
import busio
import adafruit_tlv493d

i2c = busio.I2C(1,0)
tlv = adafruit_tlv493d.TLV493D(i2c)

while True:
    print("X: %s, Y:%s, Z:%s uT"%tlv.magnetic)
    time.sleep(1)