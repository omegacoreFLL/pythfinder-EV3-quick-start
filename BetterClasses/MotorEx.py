from pybricks.tools import wait, StopWatch
from pybricks.ev3devices import Motor
from pybricks.parameters import Stop
from pybricks.hubs import EV3Brick
import math

from BetterClasses.ButtonsEx import *
from BetterClasses.ErrorEx import *
from BetterClasses.MathEx import * 
from TankDrive.constants import *

#instead of an enum
class Action:
    def __init_(self, action):
        self.RUN = self.RUN_TIME = self.RUN_ANGLE = self.RUN_TARGET = self.RUN_UNTIL_STALLED = self.DC = False

        if action == 'RUN':
            self.RUN = True
        elif action == 'RUN_TIME':
            self.RUN_TIME = True
        elif action == 'RUN_ANGLE':
            self.RUN_ANGLE = True
        elif action == 'RUN_TARGET':
            self.RUN_TARGET = True
        elif action == 'RUN_UNTIL_STALLED':
            self.RUN_UNTIL_STALLED = True
        elif action == 'DC':
            self.DC = True
        else: raise Exception("""not a valid 'action'. Choose one of these options:
                            - RUN
                            - RUN_TIME
                            - RUN_ANGLE
                            - RUN_TARGET
                            - RUN_UNTIL_STALLED
                            - DC
        """)

#command a run type to specified motor, in between certain percents of another action
#   made to replicate threading, in form of multitasking
#   percent is then computed into distances and run when scheduled
class Command:
    def __init__(self, motor, run_type, speed, value = 0, one_time_use = False, start_percent = 0, end_percent = 100):
        isType([motor, run_type, speed, start_percent, value, one_time_use, end_percent],
                 ["motor", "run_type", "speed", "start_percent", "value", "one_time_use", "end_percent"], 
                 [Motor, str, [int, float], [int, float], [int, float], bool, [int, float]])

        self.__motor = motor
        self.__run_type = run_type
        self.__value = value
        self.__speed = speed
        
        self.__numberOfCalls = 0
        self.__one_time_use = one_time_use
        
        self.__start_percent = start_percent
        self.__end_percent = end_percent

        self.__start_distance = 0
        self.__end_distance = 0
        self.__has_build = False
    
    def calculate(self, total_distance):
        isType([total_distance], ["total_distance"], [[int, float]])

        self.__start_distance = self.__start_percent / 100 * total_distance
        self.__end_distance = self.__end_percent / 100 * total_distance
        self.__has_build = True
    

    
    def __start(self):
        if not self.__one_time_use or self.__number_of_calls < 1:

            if self.__run_type == 'RUN':
                self.__motor.run(speed = self.__speed)

            elif self.__run_type == 'RUN_TIME':
                self.__motor.run_time(speed = self.__speed, time = self.__value, wait = False)

            elif self.__run_type == 'RUN_ANGLE':
                self.__motor.run_angle(speed = self.__speed, rotation_angle = self.__value, wait = False)

            elif self.__run_type == 'RUN_TARGET':
                self.__motor.run_target(speed = self.__speed, target_angle = self.__value, wait = False)

            elif self.__run_type == 'RUN_UNTIL_STALLED':
                self.__motor.run_until_stalled(speed = self.__speed, then = Stop.BRAKE)

            elif self.__run_type == 'DC':
                self.__motor.dc(duty = self.__speed)

        self.__numberOfCalls += 1
    
    def __stop(self, stop_type = Stop.BRAKE):
        if self.__run_type == 'RUN' or self.__run_type == 'DC':

            if stop_type == Stop.BRAKE:
                self.__motor.brake()

            elif stop_type == Stop.HOLD:
                self.__motor.hold()

            elif stop_type == Stop.COAST:
                self.__motor.coast()
    


    def update(self, distance):
        if not self.__has_build:
            __throw_initialization_error()
        isType([distance], ["distance"], [[int, float]])

        if abs(distance - self.__start_distance) < 1:
            self.__start()
        elif abs(distance - self.__end_distance) < 1:
            self.__stop()
    

    @staticmethod
    def __throw_initialization_error():
        raise Exception("NOT INITIALIZED!! ----- please use '.build()' function")
    
    
