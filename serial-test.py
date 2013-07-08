import serial
import time
serial = serial.Serial("/dev/ttyUSB1", baudrate=9600)

while True:
        serial.write("foo")
        time.sleep(10)
