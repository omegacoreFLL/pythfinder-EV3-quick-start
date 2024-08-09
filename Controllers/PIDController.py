
from pybricks.tools import StopWatch

# generic PID controller
class PIDController():
    def __init__(self, kP: float = 0, kI: float = 0, kD: float = 0):
        self.__kP = kP
        self.__kD = kD
        self.__kI = kI

        self.__integral = 0

        self.__current_time = 0

        self.__past_error = 0
        self.__past_time = 0
    
        self.__derivative_timer = StopWatch()
    
    def setCoefficients(self, kP: float | None = None, 
                              kI: float | None = None, 
                              kD: float | None = None):
        if not kP == None: self.__kP = kP
        if not kI == None: self.__kI = kI
        if not kD == None: self.__kD = kD

    def calculate(self, error: float):
        self.__current_time = self.__derivative_timer.time()
        self.__integral += error

        power = (self.__kP * error + # proportional
                 self.__kD * (error - self.__past_error) / (self.__current_time - self.__past_time + 0.001) + # derivative
                 self.__integral * self.__kI) # integral
  
        self.__past_time = self.__current_time
        self.__past_error = error

        return power

