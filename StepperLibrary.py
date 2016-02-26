# -*- coding: utf-8 -*-
"""
Python interface to a RoHS 28BYJ-48 stepper motor for a dragonboard410c

Created on Fri Feb 26 08:29:25 2016

@platform: linux
@author: Bill Odefey
@version: 0.1

"""
from GPIOLibrary import GPIOProcessor
import math
import time

class StepperMotor:
    # Stepper motor switching sequence
    seq = [[1,0,0,0], [1,1,0,0], [0,1,0,0], [0,1,1,0],
           [0,0,1,0], [0,0,1,1], [0,0,0,1], [1,0,0,1]]

    def __init__(self, pin1=24, pin2=28, pin3=25, pin4=33):
        """Initialize the interface passing the four GPIO pins
           to connect to.  Be sure to subtract 902 from the pin
           out diagram.  For example, GPIO pin 29 corresponds to 
           pin out 926.  To use this pin pass 926-902 or 24
        """
        self.GP = GPIOProcessor()
        self.pin1 = self.GP.getPin(pin1)
        self.pin2 = self.GP.getPin(pin2)
        self.pin3 = self.GP.getPin(pin3)
        self.pin4 = self.GP.getPin(pin4)
        self.pinl = [self.pin1, self.pin2, self.pin3, self.pin4]

        for k in range(4):
            self.pinl[k].out()

        self.speed = 100.0

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self,speed):
        if speed < 0:
            self.__speed = 0.0
        elif speed > 100:
            self.__speed = 100.0
        else:
            self.__speed = float(speed)


    def cleanup(self):
        """cleanup must be the last call to the class so that all
           GPIO pins are properly released.
        """
        self.GP.cleanup()

    def move(self, degrees=360):
        """Move the stepper motor shaft dgrees.  If degrees is negative
           the shaft will spin in reverse.
        """
        pinl = list(self.pinl)
        if degrees < 0:
            pinl.reverse()
            degrees = abs(degrees)

        steps_per_deg =4076.0/360.0
        steps = int(steps_per_deg * degrees)

        delay = 0.03 / self.speed

        for k in range(steps):
            seq_inx = k % 8
            # print("seq_inx= {0:2d}".format(seq_inx))
            for j in range(4):
                # print("\t Pin= {0:d}".format(j))
                # print("\t Value= {0:d}".format(StepperMotor.seq[seq_inx][j]))
                pinl[j].setValue(StepperMotor.seq[seq_inx][j])
                time.sleep(delay)

if __name__ == "__main__":
    motor = StepperMotor()

    try:
        motor.move(180)
        time.sleep(2)

        motor.speed = 10
        motor.move(-90)

    finally:
        motor.cleanup()




