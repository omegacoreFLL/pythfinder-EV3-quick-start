# importing all the pybricks stuff

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.media.ev3dev import SoundFile, ImageFile
import math

from Controllers.RunController import *
from BetterClasses.TelemetryEx import *
from BetterClasses.ButtonsEx import *
from BetterClasses.MathEx import * 
from BetterClasses.LedEx import *
from TankDrive.constants import *
from TankDrive.odometry import *

# core class, assuming the most common configuration of an ev3 FLL robot:
#               - 2 driving motors
#               - 2 free / task motors (for attachments)
#               - 2 color sensors, symmetrical to an imaginary middle line, in front of the robot
#               - 1 gyro sensor
class Robot:
    def __init__(self):
        self.brick = EV3Brick()

        self.leftTask = Motor(ltPort, positive_direction = Direction.COUNTERCLOCKWISE)
        self.leftDrive = Motor(ldPort)
        self.leftColor = ColorSensor(lcPort)

        self.rightTask = Motor(rtPort, positive_direction = Direction.COUNTERCLOCKWISE)
        self.rightDrive = Motor(rdPort)
        self.rightColor = ColorSensor(rcPort)

        self.gyro = GyroSensor(gyroPort)
        
        self.gamepad = ButtonEx(self.brick)
        self.telemetry = TelemetryEx(self.brick)
        self.run_control = RunController(self.gamepad, self.brick, self.telemetry)
        self.localizer = TwoWheelLocalizer(self.leftDrive, self.rightDrive, self.gyro, upside_down_gyro = True)

        self.led_control = LedEx(self.brick)
        self.led_control.addTakeYourHandsOffColor(None)

        self.fail_switch_timer = StopWatch()
        self.voltage = 0
        self.fail_switch_time = 0
    


    def normalizeVoltage(self, power):
        if self.voltage != 0:
            return power * MAX_VOLTAGE / self.voltage
        return power
    
    def resetFailSwitch(self, fst):
        self.fail_switch_timer.reset()
        self.fail_switch_time = fst
    
    def failSwitchStop(self):
        if msToS(self.fail_switch_timer.time()) > self.fail_switch_time:
            return True 
        return False

    def setWheelPowers(self, left, right, sensitivity = 1):
        self.leftDrive.dc(clipMotor(self.normalizeVoltage(left * sensitivity)))
        self.rightDrive.dc(clipMotor(self.normalizeVoltage(right * sensitivity)))
    
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
        if resetLeft:
            self.leftTask.reset_angle(0)
        if resetRight:
            self.rightTask.reset_angle(0)



    def updateOdometry(self):
        self.localizer.update()
    
    def updateRuns(self):
        self.run_control.update()

    def update(self):
        self.voltage = self.brick.battery.voltage() / 1000
        self.localizer.update()
        self.run_control.update()
        


    def showcaseAngle(self):
        self.telemetry.addData('angle (deg): ', self.localizer.angle)

    def showcaseVel(self):
        self.telemetry.addData('vel: ', self.localizer.getVelocity())

    def showcaseVoltage(self):
        self.telemetry.addData('V: ', self.voltage)

    def showcasePose(self):
        self.telemetry.addData('x: ', self.localizer.getPoseEstimate().x)
        self.telemetry.addData('y: ', self.localizer.getPoseEstimate().y)
        self.telemetry.addData('deg: ', self.localizer.getPoseEstimate().head)

    def showcaseDeltas(self):
        self.telemetry.addData('delta L: ', self.localizer.deltaL)  
        self.telemetry.addData('delta R: ', self.localizer.deltaR)  
        self.telemetry.addData('delta angle: ', self.localizer.deltaAngle)
    
    def printPose(self):
        print('x: ', self.localizer.getPoseEstimate().x)
        print('y: ', self.localizer.getPoseEstimate().y)
        print('deg: ', self.localizer.getPoseEstimate().head)

    def printVel(self):
        print('velocity: ', self.localizer.getVelocity() * 100)   