
from pybricks.tools import wait, StopWatch
import math

from Controllers.RunController import *
from BetterClasses.ButtonsEx import *
from BetterClasses.MotorEx import *
from BetterClasses.MathEx import * 
from TankDrive.constants import *
from TankDrive.pathing import *
from robot import *


#create the main robot object here
core = Robot()


#default BEFORE / AFTER run functions. Not mandatory functions
def start_run():
    global core

    if zeroBeforeEveryRun:
        core.localizer.zero()
    
    if takeHandsOff:
        core.led_control.take_your_hands_off()
        wait(sToMs(time_to_take_hands_off))
    
    core.led_control.in_progress()

def stop_run():
    global core

    core.led_control.not_started()
    core.brick.screen.clear()



#create functions for each run you want to do
def run1():
    return 0

def run2():
    return 0

def run3():
    return 0

def run4():
    return 0

def run5():
    return 0

def run6():
    return 0

def run7():
    return 0

#main loop function. Need to be called on loop in ---main.py---
def loop():
    if core.run_control.entered_center:
        core.led_control.entered_center()
    else: core.led_control.not_started()
    core.update()


#test...
def dummy():
    wait(1000)
    return 0

def test():
    inLineCM(40, core, tangential_angle = 45, threshold = 6, interpolating = True, inOtherFunction = True, accelerating = True,
            listOfCommands = [Command(motor = core.leftTask, run_type = "DC", speed = 80, start_percent = 60)]
    )
    inLineCM(40, core, tangential_angle = 10, threshold = 6, interpolating = True, inOtherFunction = True, accelerating = True,
            listOfCommands = [Command(motor = core.leftTask, run_type = "DC", speed = 80)]
    )
    inLineCM(40, core, tangential_angle = -20, threshold = 6, interpolating = True, inOtherFunction = False, accelerating = True,
            listOfCommands = [Command(motor = core.leftTask, run_type = "DC", speed = 80, end_percent = 50)]
    )

    core.printPose()


#create a list of ---Run--- objects, binded to a button (NOT ---Button.CENTER---), giving a function
#         and optional ---oneTimeUse--- and  ---with_center---- combination
run_list = [Run(Button.UP, function = test, oneTimeUse =  False, with_center = False),
            Run(Button.LEFT, function = dummy, oneTimeUse = False, with_center = False),
            Run(Button.DOWN, function = dummy, oneTimeUse = False, with_center = False),
            Run(Button.DOWN, function = dummy, oneTimeUse = False, with_center = False)]

#MANDATORY!!! add a run list to the run controller from the robot class
#               otherwise, you'll get an error. Add start / stop functions if you want
core.run_control.addRunList(run_list)
core.run_control.addBeforeEveryRun(function = start_run)
core.run_control.addAfterEveryRun(function = stop_run)

