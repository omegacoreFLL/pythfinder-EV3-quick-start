from pybricks.ev3devices import ColorSensor

from BetterClasses.EdgeDetectorEx import *
from Settings.constants import *

#enhanced color sensor class, with an edge detector for reaching the target color
#   works just with reflection (for now). Maybe we'll generalize a bit more, if needed


class ColorSensorEx():
    def __init__(self, colorSensor: ColorSensor, 
                       target_reflection: int = 7, 
                       threshold: int = 1):
    
        self.__colorSensor = colorSensor
        self.setTargetReflection(target_reflection)
    
        self.detector = EdgeDetectorEx()
        self.__threshold = threshold

        self.error = 0
        self.reading = 0
    
    def setTargetReflection(self, target_reflection: int | None):
        self.__target_reflection = target_reflection
    
    def update(self):
        # gets the value of reflection
        self.reading = self.__colorSensor.reflection()

        # updates the reflection error 
        self.error = self.__target_reflection - self.reading

        self.detector.set(self.onColor())
        self.detector.update()
    
    def onColor(self):
        return abs(self.error) <= abs(self.__threshold)
    
