from pybricks.tools import StopWatch
from pybricks.parameters import Stop

from Controllers.PIDController import *
from BetterClasses.MathEx import *
from Settings.constants import *
from robot import *

import threading

# MycroPython implementation of the PythFinder builder file.
#
# It is constructed to reduce compiling time for low performance
#   processors, like the one inside the EV3 brick. 
#


# simplified implementation of markers.
class Marker():
    def __init__(self, time: int, fun: function):
        self.value = time
        self.fun = fun
    
    def do(self):
        try: self.fun()
        except: print("\n\nexcuse me, what? \nprovide a method in the 'Marker' object with the value '{0}'"
                      .format(self.value))


# simplified implemetation of motion states.
class MotionState():
    def __init__(self, velocities: tuple, heading: float):

        self.velocities = velocities # [-100, 100] ; tuple -> (left, right)
        self.head = heading # float

class Trajectory():

    # the default constructor for trajectories. Allows empty trajectories too.
    def __init__(self):
        
        self.head_controller = PIDController(kP = kP_head, kD = kD_head, kI = 0)
        self.markers = None
        self.states = None

        self.start_pose = None
        self.end_pose = None

        self.TRAJ_TIME = None

    # reads the values constructed by PythFinder. It NEEDS to match generating format.
    # the right format is:
    #       line 1: nr of steps
    #       line 2: pairs of: LEFT speed - RIGHT speed - heading DEG - consecutive copies
    #
    # takes the name of the text file you want the data to be read from.
    # ALL FILES ARE LOOKED FOR IN THE --- Trajectory/TXT --- PATH

    def read(self, file_name):
        print('\n\nreading sweet data from {0}.txt'.format(file_name))
        elapsed = StopWatch()

        self.states = []
        if self.markers == None:
            self.markers = []
        
        with open('Trajectory//TXT//{0}.txt'.format(file_name), 'r') as f:
            lines = f.readlines()
        opening_time = msToS(elapsed.time())
        print("\nactual line reading: {0}s".format(opening_time))
        
        # first line contains marker info
        marker_times = lines[0].split()

        i = 0

        # iterate through all given timestamps
        for each in marker_times:
            try: 
                self.markers[i].value = int(each) # if a marker exists, set the time
            except: self.markers.append(Marker(time = int(each), fun = None)) # if not, create one
            finally: i += 1
        
        first = msToS(elapsed.time())
        print("\nfirst line reading: {0}s".format(first - opening_time))

        # second line is the step size
        steps = int(lines[1])
        
        second = msToS(elapsed.time())
        print("\nsecond line reading: {0}s".format(second - first))
        

        other = lines[2].split()


        third = msToS(elapsed.time())
        print("\nsplitting 3rd line: {0}s".format(third - second))

        length = len(other)
        #the other lines are 'state' values
        for i in range(0, length, 4):

            LEFT = float(other[i])
            RIGHT = float(other[i + 1])
            HEAD = float(other[i + 2])
            copies = int(other[i + 3])

            self.states.extend(MotionState(
                velocities = (LEFT, RIGHT), heading = HEAD)
                        for _ in range(copies * steps))


        
        self.TRAJ_TIME = len(self.states)
        fourth = msToS(elapsed.time())

        print("\n\ndata collected... now let's get icecream 🥰")
        print("duration: {0}s".format(fourth - third))
        print("\n\ntotal time: {0}s".format(fourth))

        return self

    # set the actions you want the markers to do
    def withMarkers(self, fun):
        # one single function
        if not isinstance(fun, tuple): 
            if self.markers == None:
                self.markers = [Marker(time = None, fun = fun)] # you don't know the time, yet
            else: self.markers[0].fun = fun

            return self
        
        # multiple functions (stored inside a tuple)
        if self.markers == None: 
            self.markers = []
        
        i = 0
        
        # iterate through all given functions
        for each in fun:
            try: self.markers[i].fun = each # if a marker exists, set the function
            except: 
                self.markers.append(Marker(time = None, fun = each)) # if not, create one
            finally: i += 1
        
        return self



    def follow(self, robot: Robot, telemetry: bool = False):
        if self.TRAJ_TIME == 0 or self.TRAJ_TIME is None: # empty trajectory
            print('\n\nsomething is empty :(')
            print('it may be the trajectory')
            print("you'll never know...")
            return 0
        
        if telemetry:
            print('\n\nFOLLOWING TRAJECTORY...')
        
        self.marker_number = len(self.markers)
        self.marker_iterator = 0

        robot.zero()
        self.__realFollow(robot)
        robot.setDriveTo(Stop.BRAKE)

        robot.leftTask.stop()
        robot.rightTask.stop()
        
        # markers from last miliseconds or beyond the time limit
        while self.marker_iterator < self.marker_number:
            marker = self.markers[self.marker_iterator]

            if marker.value > self.TRAJ_TIME:
                print('\nThe marker number {0} exceded the time limit of {1}ms with {2}ms'
                      .format(self.marker_iterator + 1, self.TRAJ_TIME, marker.value - self.TRAJ_TIME))

            threading.Thread(target = marker.do).start()
            self.marker_iterator += 1


        if telemetry:
            print('\n\nTRAJECTORY COMPLETED! ;)')

    def __realFollow(self, robot: Robot):
        marker = (Marker(0, 0) if self.marker_number == 0 else
                        self.markers[self.marker_iterator])

        time = 0
        timer = StopWatch()

        while time < self.TRAJ_TIME:
            time = timer.time()
            
            try: state = self.states[time]
            except: continue

            heading = robot.getHeading()
            target_angle = state.head

            if time >= marker.value and self.marker_iterator < self.marker_number:
                threading.Thread(target = marker.do).start()
                self.marker_iterator += 1
                
                try: marker = self.markers[self.marker_iterator]
                except: pass
            
            LEFT, RIGHT = state.velocities
            
            if LEFT == 0 and RIGHT == 0:
                robot.setDriveTo(Stop.BRAKE)
        
            head_error = findShortestPath(heading, target_angle)
            correction = self.head_controller.calculate(head_error) * robot.config.PID_multiplier

            LEFT -= correction
            RIGHT += correction

            robot.setWheelPowers(LEFT, RIGHT)
