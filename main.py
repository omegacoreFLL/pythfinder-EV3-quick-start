#!/usr/bin/env pybricks-micropython

from pybricks.tools import wait, StopWatch
import math

from Controllers.RunController import *
from BetterClasses.ButtonsEx import *
from BetterClasses.MotorEx import *
from BetterClasses.MathEx import * 
from TankDrive.constants import *
from TankDrive.pathing import *
from RunManager import *
from robot import *


#delete comments to see the frequency of one full loop
frequency_timer = StopWatch()
start_loop_time = 0

while True:
    loop() 

    #end_loop_time = frequency_timer.time()
    #print("Frequency: {:.2f} loops / second".format(1000 / (end_loop_time - start_loop_time)))
    #start_loop_time = end_loop_time
    
    
