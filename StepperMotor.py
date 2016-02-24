from GPIOLibrary import GPIOProcessor
import time
import math

# DB410c GPIO pin list
outl = []

# Stepper motor switching sequence
seq = [[1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0],
       [0,0,1,0], [0,0,1,1], [0,0,0,1], [1,0,0,1]]

stepAngle = 5.625
delay = 0.0003
#delay = 1

GP = GPIOProcessor()

try:
    # Use pins 231, 33, 30, and 34 to control motor
    out0 = GP.getPin29()  # Blue
    out1 = GP.getPin33()  # Pink
    out2 = GP.getPin30()  # Yellow
    out3 = GP.getPin34()  # Orange

    outl = [out0, out1, out2, out3]
    outl.reverse()

    # Set the pin direction to out
    for k in range(4):
        outl[k].out()

    # Rotation in degrees
    degrees = 90
    steps_per_deg =4076.0/360.0
    steps = math.floor(steps_per_deg * degrees)

    for k in range(steps):
        # print("Step: {0:2d}".format(k))
        seq_inx = k % 8
        for j in range(4):
            outl[j].setValue(seq[seq_inx][j])
            time.sleep(delay)

finally:
    GP.cleanup()
