from pybricks.parameters import Color
from pybricks.hubs import EV3Brick


# default values. You can set them any of these variants:
#    [Color.RED, Color.GREEN, Color.ORANGE, None] ONLY
default_NOT_STARTED_color = Color.RED
default_TAKE_YOUR_HANDS_OFF_color = None
default_IN_PROGRESS_color = Color.GREEN
default_ENTERED_CENTER_color = Color.ORANGE



# led control center
class LedEx():
    def __init__(self, brick: EV3Brick):
        self.__brick = brick

        self.__not_started_color = default_NOT_STARTED_color
        self.__take_your_hands_off_color = default_TAKE_YOUR_HANDS_OFF_color
        self.__in_progress_color = default_IN_PROGRESS_color
        self.__entered_center_color = default_ENTERED_CENTER_color


    def addNotStartedColor(self, color: Color):
        self.__not_started_color = color
        return self
    
    def addTakeYourHandsOffColor(self, color: Color):
        self.__take_your_hands_off_color = color
        return self
    
    def addInProgressColor(self, color: Color):
        self.__in_progress_color = color
        return self
    
    def addEnteredCenter(self, color: Color):
        self.in_entered_center = color
        return self
    


    def not_started(self):
        if self.__not_started_color == None:
            self.off()
        else: self.__brick.light.on(self.__not_started_color)
         
    def take_your_hands_off(self):
        if self.__take_your_hands_off_color == None:
            self.off()
        else: self.__brick.light.on(self.__take_your_hands_off_color)

    def in_progress(self):
        if self.__in_progress_color == None:
            self.off()
        else: self.__brick.light.on(self.__in_progress_color)
    
    def entered_center(self):
        if self.__entered_center_color == None:
            self.off()
        else: self.__brick.light.on(self.__entered_center_color)



    def off(self):
        self.__brick.light.off()
 
    def setColor(self, color: Color):
        self.__brick.light.on(color)
