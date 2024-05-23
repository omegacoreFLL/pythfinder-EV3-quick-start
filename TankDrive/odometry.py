from pybricks.ev3devices import Motor, GyroSensor
from pybricks.tools import StopWatch

from BetterClasses.MathEx import *
from TankDrive.constants import *

import math


def __encoderTicksToCM(ticks):
    return ticks * GEAR_RATIO * 2 * math.pi * WHEEL_RADIUS / TICKS_PER_REVOLUTION

#odometry class using the two encoders from the wheel motors and the gyro
#   parameters: left & right motor objects, gyro object and a boolean for gyro orientation 
#                                                           (because our gyro is upside down)
class TwoWheelLocalizer:

    def __init__(self, left, right, gyroscope, upside_down_gyro = False):

        self.__pose = Pose(0, 0, 0)
        self.__pastPose = Pose(0, 0, 0)

        self.__left_encoder = left
        self.__right_encoder = right
        self.__gyro = gyroscope
        self.__timer = StopWatch()

        self.__poseL, self.__poseR, self.__angle,  self.__pastPoseL, self.__pastPoseR, self.__pastAngle,  self.__deltaL, self.__deltaR, self.__deltaAngle = [
            0, 0, 0,     0, 0, 0,     0, 0, 0 ]

        self.__time, self.__vel, self.__pastTime,  self.__pastVel, self.__deltaTime, self.__deltaVel,  self.distance, self.__pastDistance, self.__deltaDistance = [
            0, 0, 0,     0, 0, 0,    0, 0, 0 ]
        
        self.__gyro_offset = 0
        if upside_down_gyro:
            self.__gyro_direction = -1
        else: self.__gyro_direction = 1



    def setPoseEstimate(self, newPose):

        newPose.head = normalizeDegrees(newPose.head)
        self.__gyro_offset = self.__gyro.angle() + newPose.head
        self.__pose = self.__pastPose = Pose(newPose.x, newPose.y, newPose.head)

        self.__pastPoseL, self.__pastPoseR, self.__pastAngle, self.__pastTime, self.__pastDistance, self.__pastVel = [
            self.__poseL, self.__poseR, self.__angle, self.__time, self.__deltaDistance, self.__vel ]



    def zeroTimer(self):
        self.__timer.reset()
    
    def zeroEncoders(self):
        self.__left_encoder.reset_angle(0)
        self.__right_encoder.reset_angle(0)
    
    def zeroGyro(self):
        self.__gyro.reset_angle(0)
    
    def zeroDistance(self):
        self.distance = 0
    
    def zeroPose(self):
        self.__gyro_offset = self.__gyro.angle()
        self.__pose = self.__pastPose = Pose(0, 0, 0)

        self.__pastPoseL = self.__pastPoseR = self.__pastAngle = self.__pastTime = self.__pastDistance = self.__pastVel = 0
        self.__poseL = self.__poseR = self.__angle = self.__time = self.__deltaDistance = self.__vel = 0

    def zero(self):
        self.zeroEncoders()
        self.zeroDistance()
        self.zeroPose()
        self.zeroTimer()


    
    def updateDeltas(self):
        self.__poseL = __encoderTicksToCM(self.__left_encoder.angle())
        self.__poseR = __encoderTicksToCM(self.__right_encoder.angle())
        self.__angle = normalizeDegrees(self.__gyro.angle() * self.__gyro_direction + self.__gyro_offset)
        self.__time = self.__timer.time()

        self.__deltaL = self.__poseL - self.__pastPoseL
        self.__deltaR = self.__poseR - self.__pastPoseR
        self.__deltaAngle = self.__angle - self.__pastAngle
        self.__deltaTime = self.__time - self.__pastTime

        self.__deltaDistance = (self.__deltaL + self.__deltaR) / 2
        self.__vel = (self.__deltaL + self.__deltaR) / self.__deltaTime

        self.__pastPoseL, self.__pastPoseR, self.__pastAngle, self.__pastTime, self.__pastDistance, self.__pastVel = [
            self.__poseL, self.__poseR, self.__angle, self.__time, self.__deltaDistance, self.__vel ]
    
    def updatePose(self):
        radians = normalizeRadians(toRadians(self.__pastAngle + self.__deltaAngle / 2))

        newX = self.__pose.x + self.__deltaDistance * math.cos(radians)
        newY = self.__pose.y + self.__deltaDistance * math.sin(radians)
        newHead = normalizeDegrees(self.__angle)

        self.distance += self.__deltaDistance
        self.__pose.set(newX, newY, newHead)
    
    def update(self):
        self.updateDeltas()
        self.updatePose()
    


    def getDistance(self):
        return self.distance
    
    def getPoseEstimate(self):
        return self.__pose
    
    def getRawEncoderTicks(self):
        return (self.__left_encoder.angle(), self.__right_encoder.angle())
    
    def getVelocity(self):
        return self.__vel
    
    # used on feedforward motion to decrease loop time
    def getHeading(self):
        return normalizeDegrees(self.__gyro.angle() * self.__gyro_direction + self.__gyro_offset)






