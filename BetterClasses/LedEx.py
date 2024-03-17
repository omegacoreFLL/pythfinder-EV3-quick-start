from pybricks.parameters import Color
from BetterClasses.ErrorEx import *
from pybricks.hubs import EV3Brick
from TankDrive.constants import *

#enhanced led control class, made for different run states
#   DON'T FORGET TO CALL ---build()--- FUNCTION, else you'll get an ERROR
class LedEx():
    def __init__(self, brick):
        isType([brick], ["brick"], [EV3Brick])

        self.__brick = brick
        self.__not_started_color = default_NOT_STARTED_color
        self.__take_your_hands_off_color = default_TAKE_YOUR_HANDS_OFF_color
        self.__in_progress_color = default_IN_PROGRESS_color
        self.__entered_center_color = default_ENTERED_CENTER_color

        self.__has_build = False
    


    def addNotStartedColor(self, color):
        if not color == None:
            isType([color], ["color"], [Color])
        self.__not_started_color = color
        return self
    
    def addTakeYourHandsOffColor(self, color):
        if not color == None:
            isType([color], ["color"], [Color])
        self.__take_your_hands_off_color = color
        return self
    
    def addInProgressColor(self, color):
        if not color == None:
            isType([color], ["color"], [Color])
        self.__in_progress_color = color
        return self
    
    def addEnteredCenter(self, color):
        if not color == None:
            isType([color], ["color"], [Color])
        self.in_entered_center = color
        return self
    
    def build(self):
        self.__has_build = True
    


    def not_started(self):
        if self.__has_build:
            if self.__not_started_color == None:
                self.off()
            else: self.__brick.light.on(self.__not_started_color)
        else: __throw_initialization_error()
         
    def take_your_hands_off(self):
        if self.__has_build:
            if self.__take_your_hands_off_color == None:
                self.off()
            else: self.__brick.light.on(self.__take_your_hands_off_color)
        else: __throw_initialization_error()

    def in_progress(self):
        if self.__has_build:
            if self.__in_progress_color == None:
                self.off()
            else: self.__brick.light.on(self.__in_progress_color)
        else: __throw_initialization_error()
    
    def entered_center(self):
        if self.__has_build:
            if self.__entered_center_color == None:
                self.off()
            else: self.__brick.light.on(self.__entered_center_color)
        else: __throw_initialization_error()



    def off(self):
        if self.__has_build:
            self.__brick.light.off()
        else: __throw_initialization_error()
    
    def setColor(self, color):
        isType([color], ["color"], [Color])
        self.__brick.light.on(color)


    @staticmethod
    def __throw_initialization_error():
        raise Exception("NOT INITIALIZED!! ----- please use '.build()' function")