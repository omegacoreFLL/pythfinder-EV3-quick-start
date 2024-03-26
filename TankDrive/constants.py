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



#odometry constants
#    - W (robot width), L (robot length), TRACK_WIDTH  <---  DEPRECATED
#    - WHEEL_RADIUS, GEAR_RATIO  <---  measure those and plug them in
#    - TICKS_PER_REVOLUTION, MAX_TICKS_PER_SECOND  <---  shouldn't be changed, they're the same for all ev3 large motors
W = 0 
L = 0 
WHEEL_RADIUS = 0 
GEAR_RATIO = 1 # in / out
TICKS_PER_REVOLUTION = 360 #----DON'T CHANGE----
MAX_TICKS_PER_SECOND = 1020 #----DON'T CHANGE----

TRACK_WIDTH = 0 #not used
dW = TRACK_WIDTH / 2 #----DON'T CHANGE----



#hardware ports:
#    -lt / rt  <---  left/right task motor
#    -ld / rd  <---  left/right drive motor
#    -lc / rc  <---  left/right color sensor
ltPort, rtPort, ldPort, rdPort, gyroPort, lcPort, rcPort = (
    Port.B, Port.A, Port.C, Port.D, Port.S3, Port.S4, Port.S2
)



#VERY IMPORTANT VALUE: force runs to be done in order
do_runs_in_order = False



#tune all pid values

#tune with ---turnDeg--- function
kP_head = 0 
kD_head = 0
kS_head = 0

#tune with ---inLineCM--- function
kP_fwd = 0
kS_fwd = 0 #minimum power, basically, from [-100, 100]
kP_correction_agresive = 0
kP_correction_mild = 0
kD_correction = 0

#distance threshold for switching between PID coefficients in ---inLineCM---
forward_threshold = 0

#for complex (linked) paths, go to pose without turning first (curve motion)
kP_interpolating = 0 

#line following constants 
#    ---head--- coefficients for heading correction for ---lineSquaring--- 
#    ---line--- coefficients for the actual line follow
on_edge = 0
kP_head_lf = 0
kD_head_lf = 0
kP_line_follow = 0
kD_line_follow = 0
kI_line_follow = 0


#line squaring constants
#    -turn_rate  <---  kP coefficient for turning towards the line
#    -left_on_line, right_on_line  <--- reflection values of a black line
turn_rate = 0
left_on_line = 0
right_on_line = 0



#time allocated for a 360 deg turn
timeToTurn = 6 
failSwitchTime = 0 #----DON'T CHANGE----



#dc value from [-100, 100] for acceleration + time between increments
acceleration_dc = 2
acceleration_interval = 0.04



#used to adjust dc value on motors for a much more linear output
maxVoltage = 7.9 #----DON'T CHANGE----



#number of loops in target to confirm a successful turn
targetAngleValidation = 17 #----DON'T CHANGE---- (if your robot turns well)



#flag variables. Only ---zeroBeforeEveryRun--- implemented
#    but feel free to implement others if you find it useful
zeroBeforeEveryMove, zeroBeforeEveryRun, zeroBeforeEveryTask = False, True, False

#not used, you can use it tho
#    for example, to set all runs the same ---oneTimeUse--- in ---RunManager---
oneTimeUse = False 



#accounting for time it takes for technicians to safely remove their hands off the brick
#    -takeHandsOff  <---  activate this feature or not
#    -time_to_take_hands_off  <--- alocated time
takeHandsOff = True
time_to_take_hands_off = 0.6 



#default values. You can set them any of these variants:
#    [Color.RED, Color.GREEN, Color.ORANGE, None] ONLY
default_NOT_STARTED_color = Color.RED
default_TAKE_YOUR_HANDS_OFF_color = None
default_IN_PROGRESS_color = Color.GREEN
default_ENTERED_CENTER_color = Color.ORANGE

#default value for ---ColorSensorEx---
default_target_reflection = 0

#future feature (for a 3rd color sensor in the robot, to identify attachment color, to auto-select runs)
start_run_button = Button.CENTER
#in order of runs
run_colors = [Color.GREEN, Color.WHITE, Color.BROWN, Color.RED, Color.YELLOW, Color.BLACK, Color.BLUE, None]
