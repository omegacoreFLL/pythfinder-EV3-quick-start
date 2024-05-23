from pybricks.parameters import Port, Color, Button
import math

#--------------------------IMPORTANT--------------------------
#         default unit measures:
#               -encoder values: ticks
#               -PID constants: N/O 
#               -voltage: volts
#               -distance: cm
#               -angle: deg
#               -time: sec
#         tune all values that don't have a ----DON'T CHANGE---- marked after them
#              to match your specific robot



# odometry constants
#    - WHEEL_RADIUS, GEAR_RATIO  <---  measure those and plug them in
#    - TICKS_PER_REVOLUTION, MAX_TICKS_PER_SECOND  <---  shouldn't be changed, they're the same for all ev3 large motors
WHEEL_RADIUS = 0 
GEAR_RATIO = 1 # in / out
TICKS_PER_REVOLUTION = 360 # ----DON'T CHANGE----
MAX_TICKS_PER_SECOND = 1020 # ----DON'T CHANGE----



# hardware ports:
#    -lt / rt  <---  left/right task motor
#    -ld / rd  <---  left/right drive motor
#    -lc / rc  <---  left/right color sensor
ltPort, rtPort, ldPort, rdPort, gyroPort, lcPort, rcPort = (
    Port.B, Port.A, Port.C, Port.D, Port.S3, Port.S4, Port.S2
)



# VERY IMPORTANT VALUE: force runs to be done in order
do_runs_in_order = False


# tune with ---turnDeg--- function
kP_head = 0 
kD_head = 0
kS_head = 0



# threshold for extended color sensor usge (reflection value)
on_edge = 0



# time allocated for a 360 deg turn
timeToTurn = 6 
failSwitchTime = 0 #----DON'T CHANGE----



# used to adjust dc value on motors for a much more linear output
maxVoltage = 7.9 #----DON'T CHANGE----



# number of loops in target to confirm a successful turn
targetAngleValidation = 17 #----DON'T CHANGE---- (if your robot turns well)



# flag variables. Only ---zeroBeforeEveryRun--- implemented
#    but feel free to implement others if you find it useful
zeroBeforeEveryMove, zeroBeforeEveryRun, zeroBeforeEveryTask = False, True, False

# not used, you can use it tho
#    for example, to set all runs the same ---oneTimeUse--- in ---RunManager---
oneTimeUse = False 



# accounting for time it takes for technicians to safely remove their hands off the brick
#    -takeHandsOff  <---  activate this feature or not
#    -time_to_take_hands_off  <--- alocated time
takeHandsOff = True
time_to_take_hands_off = 0.6 



# default values. You can set them any of these variants:
#    [Color.RED, Color.GREEN, Color.ORANGE, None] ONLY
default_NOT_STARTED_color = Color.RED
default_TAKE_YOUR_HANDS_OFF_color = None
default_IN_PROGRESS_color = Color.GREEN
default_ENTERED_CENTER_color = Color.ORANGE

# default value for ---ColorSensorEx---
default_target_reflection = 0

# for a 3rd color sensor in the robot, to identify attachment color, to auto-select runs
start_run_button = Button.CENTER
# in order of runs
run_colors = [Color.GREEN, Color.WHITE, Color.BROWN, Color.RED, Color.YELLOW, Color.BLACK, Color.BLUE, None]
