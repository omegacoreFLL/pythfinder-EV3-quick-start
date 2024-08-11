# importing all the pybricks stuff

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile

from Controllers.RunController import *
from BetterClasses.TelemetryEx import *
from BetterClasses.ButtonsEx import *
from Settings.ConfigReader import *
from BetterClasses.MathEx import * 
from BetterClasses.LedEx import *
from Settings.constants import *

# core class, assuming the most common configuration of an ev3 FLL robot:
#               - 2 driving motors
#               - 2 free / task motors (for attachments)
#               - 2 color sensors, symmetrical to an imaginary middle line, in front of the robot
#               - 1 gyro sensor
class Robot:
    def __init__(self):
        self.brick = EV3Brick()
        self.config = ConfigReader()


        # left and right task motors
        try:
            self.leftTask = Motor(self.config.left_task_port, 
                                  positive_direction = self.config.left_task_direction)
        except: self.leftTask = None

        try:
            self.rightTask = Motor(self.config.right_task_port,
                                   positive_direction = self.config.right_task_direction)
        except: self.rightTask = None


        # left and right drive motors
        try:
            self.leftDrive = Motor(self.config.left_wheel_port,
                                positive_direction = self.config.left_wheel_direction)
            self.rightDrive = Motor(self.config.right_wheel_port,
                                    positive_direction = self.config.right_wheel_direction)
        except: raise Exception("You need to have TWO (2) driving motors. Please check your configuration")


        # left and right color sensors
        try: self.leftColor = ColorSensor(self.config.color_sensor_left_port)
        except: self.leftColor = None

        try: self.rightColor = ColorSensor(self.config.color_sensor_right_port)
        except: self.rightColor = None

        try: self.attachmentColor = ColorSensor(self.config.attachment_color_sensor_port)
        except: self.attachmentColor = None

        try:
            self.gyro = GyroSensor(self.config.gyro_port)
        except: raise Exception("You need to have a GYRO sensor. Please check your configuration")



        self.led_control = LedEx(self.brick)
        self.led_control.addTakeYourHandsOffColor(None)

        self.gamepad = ButtonEx(self.brick)
        self.telemetry = TelemetryEx(self.brick)
        self.run_control = RunController(self.gamepad, self.brick, self.telemetry, self.led_control)

        self.frequency_timer = StopWatch()
        self.start_loop_time = 0

        self.voltage = 0

        if up_side_down_gyro:
            self.__gyro_direction = -1
        else: self.__gyro_direction = 1

        if front_side_back_gyro:
            self.config.PID_multiplier *= -1
        else: self.config.PID_multiplier *= 1

        if not self.attachmentColor == None:
            self.run_control.addColorSensor(self.attachmentColor)
    


    def normalizeVoltage(self, power):
        if self.voltage != 0:
            return power * MAX_VOLTAGE / self.voltage
        return power



    def setWheelPowers(self, left, right):
        self.leftDrive.dc(clipMotor(self.normalizeVoltage(left)))
        self.rightDrive.dc(clipMotor(self.normalizeVoltage(right)))
    
    def setDriveTo(self, stop_type):
        if stop_type is Stop.COAST:        
            self.leftDrive.stop()
            self.rightDrive.stop()
        
        elif stop_type is Stop.BRAKE:
            self.leftDrive.brake()
            self.rightDrive.brake()
        
        elif stop_type is Stop.HOLD:
            self.leftDrive.hold()
            self.rightDrive.hold()



    def zeroTaskMotors(self, resetLeft = True, resetRight = True):
        try: 
            if resetLeft:
                self.leftTask.reset_angle(0)
        except: pass
        
        try: 
            if resetRight:
                self.rightTask.reset_angle(0)
        except: pass
    
    def zeroGyro(self):
        self.gyro.reset_angle(0)

    def zero(self):
        self.zeroGyro()
        self.zeroTaskMotors()


    
    def updateRuns(self):
        self.run_control.update()

    def update(self, loop_time: bool = False):
        if self.run_control.entered_center:
            self.led_control.entered_center()
        else: self.led_control.not_started()

        self.voltage = self.brick.battery.voltage() / 1000
        self.run_control.update()

        if loop_time:
            end_loop_time = self.frequency_timer.time()
            print("Frequency: {:.2f} loops / second".format(1000 / (end_loop_time - self.start_loop_time)))
            self.start_loop_time = end_loop_time
    


    def getHeading(self):
        return normalizeDegrees(self.gyro.angle() * self.__gyro_direction)
        


    def showcaseAngle(self):
        self.telemetry.addData('angle (deg): ', self.getHeading())

    def showcaseVoltage(self):
        self.telemetry.addData('V: ', self.voltage)