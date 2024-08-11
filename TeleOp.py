#!/usr/bin/env pybricks-micropython

from BetterClasses.EdgeDetectorEx import EdgeDetectorEx
from Settings.constants import *
from robot import Robot
import struct

# Converts input range [0, 255] to motor powers [-100, 100]
def reformat(val, src, dst):
    return ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]


# Create a robot instance
core = Robot()

# Open the Gamepad event file
# /dev/input/event3 is for PS3 gamepad
# /dev/input/event4 is for PS4 gamepad
# look at contents of /proc/bus/input/devices if either one of them doesn't work.
# use 'cat /proc/bus/input/devices' in the SSH terminal and look for the event file.
infile_path = "/dev/input/event4"




# MODIFY THE FOLLOWING VALUES AS DESIRED

# button event codes 
    # 308 - square
    # 307 - triangle
    # 304 - X
    # 305 - O
left_task_code = 308  
right_task_code = 305  

power_dc = 100              # (0, 100] - power for the motors on a button press
max_linear_power_dc = 100   # same interval - max power for the forward / backward axis of motion
max_angular_power_dc = 50   # same interval - max power for the rotational axis of motion




positive_detector = EdgeDetectorEx()
negative_detector = EdgeDetectorEx()
stop_detector = EdgeDetectorEx()

SELECTED_TASK_MOTOR = 'left'
linear_velocity = 0
angular_velocity = 0

# Open file in binary mode
with open(infile_path, "rb") as controller_input:
    FORMAT = 'llHHI'
    EVENT_SIZE = struct.calcsize(FORMAT)
    
    core.brick.light.on(Color.RED)

    event = controller_input.read(EVENT_SIZE)
    while event:
        (tv_sec, tv_usec, ev_type, code, value) = struct.unpack(FORMAT, event)

        if ev_type == 3:  # Stick movement
            if code == 1:  # Left stick vertical
                linear_velocity = reformat(value, (0, 255), (max_linear_power_dc, -max_linear_power_dc))
            elif code == 3:  # Right stick horizontal
                angular_velocity = reformat(value, (0, 255), (max_angular_power_dc, -max_angular_power_dc))
            elif code == 16:
                stop_detector.set(value == 4294967295)  # D-pad left
            elif code == 17:
                positive_detector.set(value == 4294967295)  # D-pad down
                negative_detector.set(value == 1)  # D-pad up
        elif ev_type == 1 and value == 1:
            if code == left_task_code:
                SELECTED_TASK_MOTOR = 'left'
            elif code == right_task_code:
                SELECTED_TASK_MOTOR = 'right'
            stop_detector.set(False)
            positive_detector.set(False)
            negative_detector.set(False)
        
        # Update edge detectors
        positive_detector.update()
        negative_detector.update()
        stop_detector.update()

        # Motor control based on edge detection
        if positive_detector.rising:
            try:
                if SELECTED_TASK_MOTOR == 'left':
                    core.leftTask.dc(power_dc)
            except: pass
            try:
                if SELECTED_TASK_MOTOR == 'right':
                    core.rightTask.dc(power_dc)
            except: pass

        elif negative_detector.rising:
            try:
                if SELECTED_TASK_MOTOR == 'left':
                    core.leftTask.dc(-power_dc)
            except: pass
            try:
                if SELECTED_TASK_MOTOR == 'right':
                    core.rightTask.dc(-power_dc)
            except: pass

        elif stop_detector.rising:
            try:
                if SELECTED_TASK_MOTOR == 'left':
                    core.leftTask.dc(0)
            except: pass
            try:
                if SELECTED_TASK_MOTOR == 'right':
                    core.rightTask.dc(0)
            except: pass

        # Update drivetrain power based on joystick input
        core.setWheelPowers(linear_velocity - angular_velocity, 
                            linear_velocity + angular_velocity)

        # Read next controller input
        event = controller_input.read(EVENT_SIZE)
