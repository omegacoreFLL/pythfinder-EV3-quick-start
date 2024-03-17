from TankDrive.constants import *
from BetterClasses.MathEx import *
from BetterClasses.ErrorEx import *
from BetterClasses.ColorSensorEx import *
from BetterClasses.EdgeDetectorEx import *
from Controllers.PIDController import *
from pybricks.tools import StopWatch, wait
from pybricks.ev3devices import ColorSensor
from pybricks.parameters import Stop
from robot import *

#calculates time for completing a turn
def __normalizeTimeToTurn(deg):
    return abs(timeToTurn * deg / 360)

def turnRad(rad, robot, 
            threshold = 0.1, 
            sensitivity = 1):
    turnDeg(toDegrees(normalizeRadians(rad)), robot, threshold, sensitivity)

def turnDeg(deg, robot, 
            threshold = 0.1, 
            sensitivity = 1,
            inOtherFunction = False):


    isType([deg, robot, threshold, sensitivity], 
            ["deg", "robot", "threshold", "sensitivity"], 
            [[int, float], Robot, [int, float], [int, float]])


    threshold = abs(threshold)
    sensitivity = abs(sensitivity)
    robot.updateOdometry()
    pose = robot.localizer.getPoseEstimate()


    deg = normalizeDegrees(deg)
    head_error = findShortestPath(pose.head, deg)
    robot.resetFailSwitch(__normalizeTimeToTurn(head_error) / sensitivity)


    head_controller = PIDController(kP = kP_head, kD = kD_head, kI = 0)
    loopsInTarget = 0
    isBusy = True

    while isBusy:
        robot.updateOdometry()
        pose = robot.localizer.getPoseEstimate()


        head_error = findShortestPath(pose.head, deg)
        turn = head_controller.calculate(head_error) + signum(head_error) * kS_head


        if abs(head_error) <= threshold or robot.failSwitchStop():
            loopsInTarget = loopsInTarget + 1
        else: 
            loopsInTarget = 0
            robot.setWheelPowers(left = -turn, right = turn, sensitivity = sensitivity)

        if loopsInTarget == targetAngleValidation:
            isBusy = False
    
    if not inOtherFunction:
        robot.setWheelPowers(0, 0)
        robot.setDriveTo(Stop.BRAKE)

def inLineCM(cm, robot, inOtherFunction = False,
            threshold = 0.1, 
            sensitivity = 1, 
            correctHeading = True, tangential_angle = None,
            interpolating = False, accelerating = False,
            listOfCommands = None):

    if not inOtherFunction:
        isType([cm, robot, threshold, sensitivity, correctHeading, interpolating, accelerating],
                ["cm", "robot", "threshold", "sensitivity", "correctHeading", "interpolating", "accelerating"],
                [[int, float], Robot, [int, float], [int, float], bool, bool, bool])


        threshold = abs(threshold)
        sensitivity = abs(sensitivity)
        robot.updateOdometry()
        

    pose = robot.localizer.getPoseEstimate()
    if not tangential_angle == None:
        isType([tangential_angle], ["tangential_angle"], [[float, int]])
        facing_angle = normalizeDegrees(tangential_angle)
    else: facing_angle = pose.head
        

    queuedCommands = not (listOfCommands == None)

    if queuedCommands:
        actual_cm = cm - signum(cm) * threshold
        for command in listOfCommands:
            isType([command], ["command"], [Command])
            command.calculate(actual_cm)
    

    if not interpolating and abs(facing_angle - pose.head) > 0.4:
        turnDeg(facing_angle, robot)
        turnDeg(facing_angle, robot)

    
    head_controller = PIDController(kP = kP_correction_agresive, kD = kD_correction, kI = 0)
    fwd_controller = PIDController(kP = kP_fwd, kD = 0, kI = 0)
    robot.localizer.zeroDistance()
    isBusy = True


    while isBusy: 
        robot.updateOdometry()
        pose = robot.localizer.getPoseEstimate()


        fwd_error = cm - robot.localizer.distance
        fwd_error_abs = abs(fwd_error)
        forward = fwd_controller.calculate(fwd_error) + signum(cm) * kS_fwd


        if correctHeading:

            if interpolating:
                kP = kP_interpolating
            elif fwd_error_abs < forward_threshold:
                kP = kP_correction_mild
            else: kP = kP_correction_agresive

            head_controller.setCoefficients(kP = kP)
            head_error = findShortestPath(pose.head, facing_angle)
            correction = head_controller.calculate(head_error)
        
        else: correction = 0


        if fwd_error_abs <= threshold:
            isBusy = False
        else: robot.setWheelPowers(left = forward - correction, right = forward + correction, 
                            sensitivity = sensitivity, accelerating = accelerating)
        

        if queuedCommands:
            for command in listOfCommands:
                command.update(robot.localizer.distance)

    if not inOtherFunction:
        if abs(head_error) > 0.4:
            turnDeg(facing_angle, robot, inOtherFunction = inOtherFunction)
            turnDeg(facing_angle, robot, inOtherFunction = inOtherFunction)

        robot.setWheelPowers(0, 0)
        robot.setDriveTo(Stop.BRAKE)

def toPosition(target, robot, inOtherFunction = False,
            threshold = 0.1, headThreshold = 0.1, 
            sensitivity = 1, headSensitivity = 1,
            keepHeading = False, correctHeading = True, 
            forwards = True, interpolating = False, accelerating = False,
            listOfCommands = None):
    

    if not inOtherFunction:
        isType([target, robot, threshold, headThreshold, sensitivity, headSensitivity, keepHeading, correctHeading, forwards, interpolating, accelerating],
                ["target", "robot", "threshold", "headThreshold", "sensitivity", "headSensitivity", "keepHeading", "correctHeading", "forwards", "interpolating", "accelerating"], 
                [Pose, Robot, [int, float], [int, float], [int, float], [int, float], bool, bool, bool, bool, bool])
        
        
        threshold = abs(threshold)
        headThreshold = abs(headThreshold)
        sensitivity = abs(sensitivity)
        headSensitivity = abs(headSensitivity)
        robot.updateOdometry()


    pose = robot.localizer.getPoseEstimate()
    if forwards:
        direction_sign = 1
    else: direction_sign = -1

    yError = target.x - pose.x 
    xError = target.y - pose.y 
    pointError = rotateMatrix(yError, xError, toRadians(90 * direction_sign))

    needToTravelDistance = hypot(yError, xError)
    facing_angle = toDegrees(-math.atan2(pointError.x, pointError.y))


    inLineCM(cm = direction_sign * needToTravelDistance, robot = robot, inOtherFunction = True,
                sensitivity = sensitivity, correctHeading = correctHeading, threshold = threshold,
                tangential_angle = facing_angle, interpolating = interpolating, 
                accelerating = accelerating, listOfCommands = listOfCommands)
        
    if not inOtherFunction:
        if not keepHeading:
            turnDeg(target.head, robot, sensitivity = headSensitivity, threshold = headThreshold)
            turnDeg(target.head, robot, sensitivity = headSensitivity, threshold = headThreshold)

        robot.setWheelPowers(0, 0)
        robot.setDriveTo(Stop.BRAKE)
    
def lineSquare(robot,
                sensitivity = 1,
                backing_distance = 1.5, success_threshold = 1,
                forwards = True, accelerating = False,
                time_threshold = None):


    isType([robot, sensitivity, backing_distance, success_threshold, forwards, accelerating],
            ["robot", "sensitivity", "backing_distance", "success_threshold", "forwards", "acceelerating"],
            [Robot, [int, float], [int, float], [int, float], bool, bool])


    sensitivity = abs(sensitivity)
    success_threshold = abs(success_threshold)
    backing_distance = abs(backing_distance)
    robot.updateOdometry()
    facing_angle = robot.localizer.getPoseEstimate().head

    left_color = ColorSensorEx(robot.leftColor, target_reflection = left_on_line)
    right_color = ColorSensorEx(robot.rightColor, target_reflection = right_on_line)


    if forwards:
        direction_sign = 1
    else: direction_sign = -1


    exitByTime = False
    exitBySuccess = False
    
    times_reached = 0
    turn_direction = 0
    isBusy = True

    
    if not time_threshold == None:
        time_threshold = abs(time_threshold)
        time_exit = True
    else: time_exit = False
    exit_timer = StopWatch()

    
    driveUntilOnColor(robot, left_on_line, right_on_line, inOtherFunction = True,
                        sensitivity = sensitivity, forwards = forwards, accelerating = accelerating)
    exit_timer.reset()


    while isBusy:
        robot.updateOdometry()
        pose = robot.localizer.getPoseEstimate()
        left_color.update()
        right_color.update()

        left_on_color = left_color.onColor()
        right_on_color = right_color.onColor()
        left_reading = left_color.reading
        right_reading = right_color.reading

        actual_turn_rate = abs(left_reading - right_reading) * turn_rate


        if not left_on_color and right_on_color:
            times_reached = 0
            turn_direction = 1

        elif left_on_color and not right_on_color:
            times_reached = 0
            turn_direction = -1

        elif left_on_color and right_on_color:
            times_reached += 1
            turn_direction = 0



    
        if time_exit:
            if msToS(exit_timer.time()) > time_threshold:
                exitByTime = True
                isBusy = False

                robot.setWheelPowers(0, 0)
                robot.setDriveTo(Stop.BRAKE)
                print("exit by time")
            
        if times_reached >= success_threshold:
            exitBySuccess = True
            isBusy = False

            robot.setWheelPowers(0, 0)
            robot.setDriveTo(Stop.BRAKE)
            print("exit by success")   

        if isBusy:
            if left_color.detector.rising or right_color.detector.rising:
                inLineCM(cm = (backing_distance + 3) * -direction_sign, robot = robot, inOtherFunction = True, 
                            threshold = 3, sensitivity = 0.6)
                turnDeg(robot.localizer.getPoseEstimate().head + turn_direction * direction_sign * actual_turn_rate, robot)
                
            robot.setWheelPowers(100 * direction_sign, 100 * direction_sign, 
                        sensitivity = 0.6, accelerating = False)
    
    
    robot.setWheelPowers(0, 0)
    robot.setDriveTo(Stop.BRAKE)
        
def lineFollow(robot, sensor,
                sensitivity = 1, time = 10,
                forwards = True, left_curve = True):
    
    isType([robot, sensor, sensitivity, time, forwards, left_curve],
            ["robot", "sensor", "sensitivity", "time", "forwards", "left_curve"],
            [Robot, ColorSensor, [int, float], [int, float], bool, bool])
    
    sensitivity = abs(sensitivity)
    time = abs(time)
    

    if forwards:
        forward_direction = 1
    else: forward_direction = -1

    if left_curve:
        turn_direction = 1
    else: turn_direction = -1


    forwardSpeed = 60 * forward_direction * sensitivity
    exitByTime = False

    sensor_ex = ColorSensorEx(color, target_reflection = on_edge)
    color_controller = PIDController(kP = kP_line_follow, kD = kD_line_follow, kI = kI_line_follow)
    exit_timer = StopWatch()


    while not exitByTime:
        robot.updateOdometry()
        sensor_ex.update()

        turnSpeed = color_controller.calculate(sensor_ex.error) * turn_direction 
        print(turnSpeed)

        robot.setWheelPowers(left = forwardSpeed - turnSpeed, right = forwardSpeed + turnSpeed)

        if msToS(exit_timer.time()) > time:
            exitByTime = True
      

    robot.setWheelPowers(0, 0)
    robot.setDriveTo(Stop.BRAKE)

def driveUntilOnColor(robot, left_on_color, right_on_color,
                        inOtherFunction = False,
                        sensitivity = 1, threshold = 1,
                        accelerating = False, forwards = True,
                        time = None):


    if not inOtherFunction:
        isType([robot, left_on_color, right_on_color, sensitivity, threshold, accelerating, forwards],
                ["robot", "left_on_color", "right_on_color", "sensitivity", "threshold", "accelerating", "forwards"],
                [Robot, [int, float], [int, float], [int, float], [int, float], bool, bool])
        sensitivity = abs(sensitivity)
    
        
    if forwards:
        direction_sign = 1
    else: direction_sign = -1
    

    if not time == None:
        timeExit = True
        isType([time], ["time"], [int, float])
        time = abs(time)
    else: timeExit = False


    robot.updateOdometry()
    facing_angle = robot.localizer.getPoseEstimate().head

    left_color = ColorSensorEx(robot.leftColor, target_reflection = left_on_color, threshold = threshold)
    right_color = ColorSensorEx(robot.rightColor, target_reflection = right_on_color, threshold = threshold)
    head_controller = PIDController(kP = kP_head_lf, kD = kD_head_lf, kI = 0)
    reached_line_detector = EdgeDetectorEx()
    exit_timer = StopWatch()


    exitByTime = False
    exitBySuccess = False
    isBusy = True


    while isBusy:
        robot.updateOdometry()
        pose = robot.localizer.getPoseEstimate()
        left_color.update()
        right_color.update()

        head_error = findShortestPath(pose.head, facing_angle)
        correction = head_controller.calculate(head_error)


        if left_color.onColor() or right_color.onColor():
            reached_line_detector.set(True)
        

        reached_line_detector.update()

        if reached_line_detector.rising:
            exitBySuccess = True
            isBusy = False
        
        if timeExit:
            if msToS(exit_timer.time()) > time:
                exitByTime = True
                isBusy = False
        
        robot.setWheelPowers(100 * direction_sign - correction, 100 * direction_sign + correction, 
                    sensitivity = sensitivity, accelerating = accelerating)
    

    robot.setWheelPowers(0, 0)
    robot.setDriveTo(Stop.BRAKE)


