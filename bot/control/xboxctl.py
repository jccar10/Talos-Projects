## Code for Rasp Pi 
#   Use Xbox controller and give drive commands to the Arduinos

#import evdev
#from evdev import InputDevice, categorize, ecodes
from __future__ import print_function
import math
import serial
import time
import xbox

# initialization of global vars
MAXSPD = 80
thresh = 0.2
maxval = 1

# dimensions of robot in m
a=0.1 # distance from bot centre to front axle (x)
b=0.1 # distance from bot centre to wheel centre (y)
R=0.05

#initializes xbox controller
joy = xbox.Joystick()

lxval = 0
lyval = 0

# Format floating point number to string format -x.xxx
def fmtFloat(n):
    return '{:6.3f}'.format(n)

# Print one or more values without a line feed
def show(*args):
    for arg in args:
        print(arg, end="")
        
# Print true or false value based on a boolean, without linefeed
def showIf(boolean, ifTrue, ifFalse=" "):
    if boolean:
        show(ifTrue)
    else:
        show(ifFalse)

def scale(val, src, dst):
    return (float(val-src[0]) / (src[1]-src[0]) * (dst[1]-dst[0]) + dst[0])
            
def scale_stick(value):
    return scale(value, (0,255), (-100,100))

# front
serFR = serial.Serial("/dev/ttyACM0", 9600)
time.sleep(1)
# rear
serRE = serial.Serial("/dev/ttyACM1", 9600)
time.sleep(1)
#prints out device info at start
print(joy)

#loop and filter by event code and print the mapped label
while not joy.Back() and joy:
# Show connection status
    show("Connected:")
    showIf(joy.connected(), "Y", "N")
    # Left analog stick
    show("  Left X/Y:", fmtFloat(joy.leftX()), "/", fmtFloat(joy.leftY()))
    # Right stick
    show("  Right X/Y:", fmtFloat(joy.rightX()), "/", fmtFloat(joy.rightY()))
    # # A/B/X/Y buttons
    # show("  Buttons:")
    # showIf(joy.A(), "A")
    # showIf(joy.B(), "B")
    # showIf(joy.X(), "X")
    # showIf(joy.Y(), "Y")
    # # Dpad U/D/L/R
    # show("  Dpad:")
    # showIf(joy.dpadUp(),    "U")
    # showIf(joy.dpadDown(),  "D")
    # showIf(joy.dpadLeft(),  "L")
    # showIf(joy.dpadRight(), "R")
    
    
    
    lx = -joy.leftX()
    ly = -joy.leftY()

    rx = joy.rightX()
    ry = joy.rightY()
    

    lrval = math.sqrt(lx*lx + ly*ly)
    lrphi = math.atan2(lx, -ly)

    if (lrval < thresh):
        lrval = 0
    elif (lrval > maxval):
        lrval = maxval
    else:
        lrval = (lrval - thresh) / (maxval - thresh) * maxval
        


    #convert to drive components for front wheels
        
    ## for polar coords:
    #fwd_comp = lrval * math.cos(lrphi) / math.sqrt(2)
    #rgt_comp = lrval * math.sin(lrphi) / math.sqrt(2)


    # for reading stick pos directly:
    x_comp = ly
    y_comp = lx
    rot_comp = rx
    
    # adjust speed of rotation with variable - nominally represents radius of wheel (R = 0.05m) but will just adjust speed of rotation
    A = -50
    B = 4*(a+b)
    # These should give a max value of 96 (if a=0.1 and b=0.1)
    FL_drive = A*(x_comp - y_comp - B*rot_comp)
    FR_drive = A*(x_comp + y_comp + B*rot_comp)

    RL_drive = A*(x_comp + y_comp - B*rot_comp)
    RR_drive = A*(x_comp - y_comp + B*rot_comp)
    
    #print("FL_drive = ", FL_drive)
    #print("FR_drive = ", FR_drive)

    #convert to integers in byte range (0,255) for forward and backward
    #drive values
    FL_drive = int(math.floor(scale(FL_drive, (-100,100), (127-MAXSPD,127+MAXSPD))))
    FR_drive = int(math.floor(scale(FR_drive, (-100,100), (127-MAXSPD,127+MAXSPD))))
    RL_drive = int(math.floor(scale(RL_drive, (-100,100), (127-MAXSPD,127+MAXSPD))))
    RR_drive = int(math.floor(scale(RR_drive, (-100,100), (127-MAXSPD,127+MAXSPD))))
    
    # show("FL_drive byte = ", FL_drive)
    # show("FR_drive byte = ", FR_drive)
    # show("RL_drive byte = ", RL_drive)
    # show("RR_drive byte = ", RR_drive)

    # front drive
    vals = []
    vals.append(str(FL_drive))
    vals.append(str(FR_drive))    
    serial_output = ','.join(vals)+';'
    show('FRONT drive:', serial_output)
    serFR.write(serial_output)

    # rear drive
    vals = []
    vals.append(str(RL_drive))
    vals.append(str(RR_drive))    
    serial_output = ','.join(vals)+';'
    show('REAR  drive:', serial_output)
    serRE.write(serial_output)

# Move cursor back to start of line
    show(chr(13))
#    time.sleep(0.1)
joy.close()
