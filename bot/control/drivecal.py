# drivecal: use up/down/left/right keys on controller to
# move vehicle for 1s in each direction. Measure actual
# movement in x,y,rotation, and use results to calibrate
#
# pdf reference to be cited here / checked in.


#import evdev
from evdev import InputDevice, categorize, ecodes
import math
import serial
import time


# set this to calibrate at this particular desired speed
MAXSPD = 48

# which direction currently moving
NONE = 0
FORWARD = 1
RIGHT = 2
BACKWARD = 3
LEFT = 4
CURRDIR = NONE

# time moving for
DRIVETIME = 5.0



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
        CURRDIR = 0;
        if event.value == 1:
            if event.code == up:
                print("up")
                CURRDIR = FORWARD;
            elif event.code == down:
                print("down")
                CURRDIR = BACKWARD;
            elif event.code == left:
                print("left")
                CURRDIR = LEFT;
            elif event.code == right:
                print("right")
                CURRDIR = RIGHT;

    if CURRDIR > NONE:
        lrval = MAXSPD
        lrphi = math.atan2(0.,1.)
        if CURRDIR == BACKWARD:
            lrphi = math.atan2(0.,-1.)
        elif CURRDIR == LEFT:
            lrphi = math.atan2(1., 0.)
        elif CURRDIR == RIGHT:
            lrphi = math.atan2(-1., 0.)

        #if (lrval < thresh):
        #    lrval = 0
        #elif (lrval > maxval):
        #    lrval = maxval
        #else:
        #    lrval = (lrval - thresh) / (maxval - thresh) * maxval
        
        #convert to drive components for front wheels
        fwd_comp = lrval * math.cos(lrphi) / math.sqrt(2)
        rgt_comp = lrval * math.sin(lrphi) / math.sqrt(2)

        FL_drive = fwd_comp * 1.0 + rgt_comp * 1.0
        FR_drive = fwd_comp * 1.0 - rgt_comp * 1.0

        RL_drive = fwd_comp * 1.0 - rgt_comp * 1.0
        RR_drive = fwd_comp * 1.0 + rgt_comp * 1.0
    
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
        
        
        time.sleep(DRIVETIME)
        CURRDIR = NONE;
        vals = []
        vals.append(str(127))
        vals.append(str(127))
        serial_output = ','.join(vals)+';'
        serFR.write(serial_output)
        serRE.write(serial_output)
