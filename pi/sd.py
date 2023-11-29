import adafruit_sdcard
import busio
import digitalio
import board


# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.CE1)
sd = adafruit_sdcard.SDCard(spi, cs)
sd.writeblocks(0, 15232)
#vfs = os.VfsFat(sd)
#os.mount(sd, "/sd")
#vfs = storage.VfsFat(sdcard)
#storage.mount(vfs, "/sd")
print("test")

# Use the filesystem as normal.
#with open("/sd/test.txt", "w") as f:
#    f.write("Hello world\n")