# testing git update II
#import evdev
from evdev import InputDevice, categorize, ecodes
import math
import serial
import time


MAXSPD = 48




#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event3')

#button code variables (change to suit your device)
sqBtn = 308
trBtn = 307
xBtn = 304
oBtn = 305

up = 544
down = 545 
left = 546
right = 547

#start = 24
#select = 49

l1 = 310
l2 = 312
r1 = 311
r2 = 313

lx = 0
ly = 1
rx = 3
ry = 4

thresh = 20
maxval = 100

lxval = 0
lyval = 0

def scale(val, src, dst):
    return (float(val-src[0]) / (src[1]-src[0]) * (dst[1]-dst[0]) + dst[0])
            
def scale_stick(value):
    return scale(value, (0,255), (-100,100))

# front
serFR = serial.Serial("/dev/ttyACM0", 9600)
# rear
serRE = serial.Serial("/dev/ttyACM1", 9600)

#prints out device info at start
print(gamepad)

#loop and filter by event code and print the mapped label
for event in gamepad.read_loop():
    
    if event.type == ecodes.EV_KEY:
        #print "KEY code = ", event.code
        if event.value == 1:
            if event.code == oBtn:
                print("O")
            elif event.code == trBtn:
                print("Tr")
            elif event.code == sqBtn:
                print("Sq")
            elif event.code == xBtn:
                print("X")

            elif event.code == up:
                print("up")
            elif event.code == down:
                print("down")
            elif event.code == left:
                print("left")
            elif event.code == right:
                print("right")
            elif event.code == l1:
                print("L1")
            elif event.code == l2:
                print("L2")

            elif event.code == r1:
                print("R1")
            elif event.code == r2:
                print("R2")
            
    elif event.type == ecodes.EV_ABS:
        val = scale_stick(event.value)
        if (1 or val < -thresh or val > thresh):
            if event.code == ry:
                ryval = val
                #print "RY = ", val
            elif event.code == rx:
                rxval = val
                #print "RX = ", val
            elif event.code == ly:
                lyval = val
                #print "LY = ", val
            elif event.code == lx:
                lxval = val
                #print "LX = ", val
            
    lrval = math.sqrt(lxval*lxval + lyval*lyval)
    lrphi = math.atan2(lxval, -lyval);

    if (lrval < thresh):
        lrval = 0
    elif (lrval > maxval):
        lrval = maxval
    else:
        lrval = (lrval - thresh) / (maxval - thresh) * maxval
        
    #print("L stick R = ", lrval)
    #print("L stick phi = ", lrphi)

    #convert to drive components for front wheels

    fwd_comp = lrval * math.cos(lrphi) / math.sqrt(2)
    rgt_comp = lrval * math.sin(lrphi) / math.sqrt(2)

    FL_drive = fwd_comp * 1.0 + rgt_comp * 1.0
    FR_drive = fwd_comp * 1.0 - rgt_comp * 1.0

    RL_drive = fwd_comp * 1.0 - rgt_comp * 1.0
    RR_drive = fwd_comp * 1.0 + rgt_comp * 1.0
    
    #print("FL_drive = ", FL_drive)
    #print("FR_drive = ", FR_drive)

    #convert to integers in byte range (0,255) for forward and backward
    #drive values
    FL_drive = int(math.floor(scale(FL_drive, (-100,100), (127-MAXSPD,127+MAXSPD))))
    FR_drive = int(math.floor(scale(FR_drive, (-100,100), (127-MAXSPD,127+MAXSPD))))
    RL_drive = int(math.floor(scale(RL_drive, (-100,100), (127-MAXSPD,127+MAXSPD))))
    RR_drive = int(math.floor(scale(RR_drive, (-100,100), (127-MAXSPD,127+MAXSPD))))
    
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

    
    #time.sleep(0.1)
