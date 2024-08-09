from pybricks.parameters import Color, Button

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


# force runs to be done in order
do_runs_in_order = False

# PID constants for heading correction
# You can change these values to match your specific configuration
#   There are lots of great tutorials online on how to tune a PID
kP_head = 3
kD_head = 0

# used to adjust dc value on motors for a much more linear output
MAX_VOLTAGE = 7.5 #----DON'T CHANGE----



# flag variables. Only ---zeroBeforeEveryRun--- implemented
#    but feel free to implement others if you find it useful
zeroBeforeEveryMove, zeroBeforeEveryRun, zeroBeforeEveryTask = False, True, False



# accounting for time it takes for technicians to safely remove their hands off the brick
#    -takeHandsOff  <---  activate this feature or not
#    -time_to_take_hands_off  <--- alocated time
takeHandsOff = True
time_to_take_hands_off = 0.6 



# for a 3rd color sensor in the robot, to identify attachment color, to auto-select runs
start_run_button = Button.CENTER
# in order of runs
run_colors = [Color.GREEN, Color.WHITE, Color.BROWN, Color.RED, Color.YELLOW, Color.BLACK, Color.BLUE, None]
