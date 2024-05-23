#!/usr/bin/env pybricks-micropython

from BetterClasses.EdgeDetectorEx import *
from Controllers.PIDController import *
from BetterClasses.MathEx import *
from TankDrive.constants import *
from robot import *
import struct



# MycroPython implementation of joystick control for EV3 robots.
# 
# It enters the internal file in which controller values are stored,
#   reads the set of data then does some manipulation to control both
#   the drivetrain and the two output motors, generally used in FLL
#   robots.



# from the input range [0, 255] to motor powers [-100, 100]
def reformat(val, src, dst):
    return (float(val-src[0]) / (src[1]-src[0])) * (dst[1]-dst[0])+dst[0]

def clip(val):
    if val < -100:
        return -100
    if val > 100:
        return 100
    return val

# create a robot instance
core = Robot()

# /dev/input/event4 is for PS4 gamepad
infile_path = "/dev/input/event4"

# button event codes
left_task_code = 304
right_task_code = 305


positive_detector = EdgeDetectorEx()
negative_detector = EdgeDetectorEx()
stop_detector = EdgeDetectorEx()


SELECTED_TASK_MOTOR = 'left'
linear_velocity = 0
angular_velocity = 0

# open file in binary mode
controller_input = open(infile_path, "rb")

FORMAT = 'llHHI'    
EVENT_SIZE = struct.calcsize(FORMAT)
event = controller_input.read(EVENT_SIZE)

core.brick.light.on(Color.RED)

while event:
    (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)
    task_power = 0

    if ev_type == 3: # stick was moved
        if code == 1: # left stick vertical
            linear_velocity = reformat(value, (0,255), (100,-100))
        
        elif code == 3: # right stick horizontal
            angular_velocity = reformat(value, (0,255), (50, -50))
        
        elif code == 17:
            if value == 1: # dpad up
                positive_detector.set(False)
                negative_detector.set(True)

                stop_detector.set(False)
            elif value == 4294967295: # dpad down
                positive_detector.set(True)
                negative_detector.set(False)

                stop_detector.set(False)
            else: # no button is pressed
                positive_detector.set(False)
                negative_detector.set(False)
        
        elif code == 16:
            if value == 4294967295: #dpad left
                stop_detector.set(True)
                positive_detector.set(False)
                negative_detector.set(False)

        
    elif ev_type == 1:
        if code == left_task_code:
            SELECTED_TASK_MOTOR = 'left'
        
        elif code == right_task_code:
            SELECTED_TASK_MOTOR = 'right'
        
    positive_detector.update()
    negative_detector.update()
    stop_detector.update()

    if positive_detector.rising: # power in the positive direction
        if SELECTED_TASK_MOTOR == 'left':
            core.leftTask.dc(100)
        elif SELECTED_TASK_MOTOR == 'right':
            core.rightTask.dc(100)
    
    if negative_detector.rising: # power in the negative direction
        if SELECTED_TASK_MOTOR == 'left': 
            core.leftTask.dc(-100)
        elif SELECTED_TASK_MOTOR == 'right':
            core.rightTask.dc(-100)
    
    if stop_detector.rising: # stop the motor
        if SELECTED_TASK_MOTOR == 'left':
            core.leftTask.dc(0)
        elif SELECTED_TASK_MOTOR == 'right':
            core.rightTask.dc(0)
    
    # from the differential drive kinematics

    left = clip(linear_velocity - angular_velocity) 
    right = clip(linear_velocity + angular_velocity)
    core.setWheelPowers(left, right)

    # update controller reading
    event = controller_input.read(EVENT_SIZE)

# exit the reading file
controller_input.close()