import os
from math import cos, sin, pi, floor
from adafruit_rplidar import RPLidar
import serial

PORT_NAME = '/dev/ttyUSB0'
lidar = RPLidar(None, PORT_NAME)
scan_data = [-1]*360

ser = serial.Serial("/dev/ttyACM0", 9600)

def process(data) :

    # print(data)

    # average 20 angles at a time for display on perimeter of 5x5 square
    
    for j in range(0,20):
        i1 = j * 18 - 9
        low = 99999; # we look for closest
        for i in range (0,18):
            val = data[(i1+i) % 360]
            if (val > 0) and  (val < low):
                low = val
        #print (j, i1, low)
            
    

try:
    print(lidar.info)
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            scan_data[min([359, floor(angle)])] = distance
        process (scan_data)
        scan_data = [-1]*360

except KeyboardInterrupt:
    print('Stopping...')
lidar.stop()
lidar.disconnect()


