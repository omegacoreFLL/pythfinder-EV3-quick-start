from TankDrive.constants import *
from BetterClasses.MathEx import *
from BetterClasses.ColorSensorEx import *
from BetterClasses.EdgeDetectorEx import *
from Controllers.PIDController import *
from pybricks.tools import StopWatch, wait
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Stop
from robot import *

# calculates time for completing a turn
def __normalizeTimeToTurn(deg):
    return abs(timeToTurn * deg / 360)

def turnDeg(deg, robot, 
            threshold = 0.1, 
            sensitivity = 1):


    threshold = abs(threshold)
    sensitivity = abs(sensitivity)

    heading = robot.localizer.getHeading()


    deg = normalizeDegrees(deg)
    head_error = findShortestPath(heading, deg)
    robot.resetFailSwitch(__normalizeTimeToTurn(head_error) / sensitivity)


    head_controller = PIDController(kP = kP_head, kD = kD_head, kI = 0)
    loopsInTarget = 0


    while not loopsInTarget == targetAngleValidation:
        heading = robot.localizer.getHeading()


        head_error = findShortestPath(heading, deg)
        turn = head_controller.calculate(head_error) + signum(head_error) * kS_head

        if abs(head_error) <= threshold or robot.failSwitchStop():
            loopsInTarget = loopsInTarget + 1
        else: 
            loopsInTarget = 0
            robot.setWheelPowers(left = -turn, right = turn, sensitivity = sensitivity)


    robot.setWheelPowers(0, 0)
    robot.setDriveTo(Stop.BRAKE)


