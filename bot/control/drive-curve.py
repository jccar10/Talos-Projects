# drive-curve: call progressively with different start points
# and record rpm of each motor as measured with only load
# mecanum wheel elevated off ground.
#
# drivetime should be 8.0s, lift up for the slower RPM to
# about 12s.
#
# fyi I made a curve from 16, 32, 48, ... 240 where our zero
# for the current design is 127/128.
#
# pdf reference to be cited here / checked in.


#import evdev
from evdev import InputDevice, categorize, ecodes
import math
import serial
import time
import numpy as np

# RANGE for testing
SIG_START = 224
SIG_STEP = 16
SIG_END = SIG_START + 2 * SIG_STEP - 1
SIG_STEPS = np.arange(SIG_START, SIG_END, SIG_STEP)

# time moving for
DRIVETIME = 8.0

# front
serFR = serial.Serial("/dev/ttyACM0", 9600)
# rear
serRE = serial.Serial("/dev/ttyACM1", 9600)

time.sleep(DRIVETIME)

#loop and filter by event code and print the mapped label
for drive in SIG_STEPS:


    FL_drive = FR_drive = drive
    RL_drive = RR_drive = drive
    print("FL_drive byte = ", FL_drive)
    print("FR_drive byte = ", FR_drive)
    print("RL_drive byte = ", RL_drive)
    print("RR_drive byte = ", RR_drive)
        
    # front drive
    vals = []
    vals.append(str(FL_drive))
    vals.append(str(FR_drive))    
    serial_output = ','.join(vals)+';'
    print('FRONT drive:', serial_output)
    serFR.write(serial_output)
        
    # rear drive
    vals = []
    vals.append(str(RL_drive))
    vals.append(str(RR_drive))    
    serial_output = ','.join(vals)+';'
    print('REAR  drive:', serial_output)
    serRE.write(serial_output)
        
        
    time.sleep(DRIVETIME)
    vals = []
    vals.append(str(127))
    vals.append(str(127))
    serial_output = ','.join(vals)+';'
    serFR.write(serial_output)
    serRE.write(serial_output)
    
