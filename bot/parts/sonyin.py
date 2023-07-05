#import evdev
from evdev import InputDevice, categorize, ecodes

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

def scale(val, src, dst):
    return (float(val-src[0]) / (src[1]-src[0]) * (dst[1]-dst[0]) + dst[0])
            
def scale_stick(value):
    return scale(value, (0,255), (-100,100))

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
        if (val < -thresh or val > thresh):
            if event.code == ry:
                print "RY = ", val
            elif event.code == rx:
                print "RX = ", val
            elif event.code == ly:
                print "LY = ", val
            elif event.code == lx:
                print "LX = ", val
            
