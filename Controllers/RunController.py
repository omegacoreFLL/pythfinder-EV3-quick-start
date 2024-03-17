from pybricks.parameters import Button, Color
from BetterClasses.ErrorEx import *
from TankDrive.constants import *
from pybricks.tools import wait
import math

#class to describe run-specific constants
class Run():
    def __init__(self, button, function, run_number = None, color = None, oneTimeUse = True, with_center = False):
        if not button == None:
            isType([button], ["button"], [Button])
            if button == Button.CENTER:
                raise Exception("can't use 'Button.CENTER' for starting a run")

        isType([oneTimeUse, with_center], 
                ["oneTimeUse", "with_center"],
                [bool, bool])
            
        self.button = button
        self.run_number = run_number
        self.runs = 0
        self.oneTimeUse = oneTimeUse
        self.with_center = with_center

        self.running = False
        self.pastRunning = False

        self.function = function
        self.color = color
        
    
    def hasJustStarted(self):
        return not self.pastRunning and self.running
    
    def hasNotStarted(self):
        return not self.pastRunning and not self.running
    
    def runable(self):
        return not self.oneTimeUse or not self.runs > 0
    
    def update(self):
        self.pastRunning = self.running
    
    def start(self):
        if self.hasJustStarted():
            self.runs +=1
            self.function()
        self.running = False
    
    def done(self):
        return self.oneTimeUse and self.runs > 0

#logic for run-selection. Don't modify things here    
class RunController():
    def __init__(self, gamepad, brick, telemetry, run_list = None):

        self.next_run = 1
        self.run_loops = 0
        self.all_oneTimeUse = True

        self.run_list = None
        if not self.run_list == None:
            self.addRunList(self.run_list)

        self.color_sensor_control = False
        self.color_sensor = None
        self.seen_color = None
        self.entered_center = False
        self.run = 1

        self.gamepad = gamepad
        self.brick = brick
        self.telemetry = telemetry

        self.beforeEveryRun = None
        self.afterEveryRun = None
    


    def addRunList(self, run_list):
        self.run_list = run_list
        self.total_runs = len(self.run_list)

        for run in range(self.total_runs):
            self.run_list[run].run_number = run + 1
            if not self.run_list[run].oneTimeUse:
                self.all_oneTimeUse = False
        
        self.__showcaseNextRun()
    
    def addBeforeEveryRun(self, function):
        self.beforeEveryRun = function
    
    def addAfterEveryRun(self, function):
        self.afterEveryRun = function

    def addColorSensor(self, sensor):
        self.color_sensor = sensor
        self.color_sensor_control = True

        if self.run_list == None:
            raise Exception("add ---run_list--- first")
        if self.total_runs > 8:
            raise Exception("too many runs, there are only 8 different colors")
        
        for run in self.run_list:
            run.button = start_run_button
            run.with_center = False
        
        self.__showcaseNextRun()
    


    def __shouldStartRun(self, run):
        if not run.runable():
            return 0
        
        run.update()
        if (run.with_center and self.entered_center) or (not run.with_center and not self.entered_center):
            if self.gamepad.wasJustPressed(run.button):
                run.running = True



    def __updateManual(self):
        if self.gamepad.wasJustPressed(Button.CENTER):
            self.entered_center = not self.entered_center

        #if same button, run the one ran fewer times
        optimal_run = Run(None, None) 
        optimal_run.runs = -1
        past_run_index = -1

        for run in range(self.total_runs):
            current_run = self.run_list[run]

            if not do_runs_in_order or run + 1 == self.next_run:

                self.__shouldStartRun(current_run)
                if current_run.hasJustStarted():

                    if optimal_run.button == None:
                        optimal_run = current_run
                        past_run_index = run

                    elif current_run.runs < optimal_run.runs:
                        self.run_list[past_run_index].running = False
                        optimal_run = current_run
                        past_run_index = run

                    else: self.run_list[run].running = False

        if not optimal_run.button == None:          
            self.__start(optimal_run)
        
    def __updateNextRun(self, current_run):
        if current_run.run_number == self.next_run:
            this_loop = self.run_loops

            verified = 0
            found = False
            while (not self.run_list[self.next_run - 1].runable() or not found) and verified <= self.total_runs:

                if self.next_run >= self.total_runs:
                    self.next_run = 1
                    self.run_loops += 1
                else: self.next_run += 1

                if self.run_list[self.next_run - 1].runable():
                    found = True
                verified += 1

    def __updateAuto(self):
        self.seen_color = self.color_sensor.color()

        for index in range(self.total_runs):

            if run_colors[index] == self.seen_color:
                current_run = self.run_list[index]
                self.__shouldStartRun(current_run)

                if current_run.hasJustStarted():
                    self.__start(current_run)
    
    def update(self):
        #skip update when done
        if self.__done():
            return 0
        
        self.gamepad.updateButtons()
        
        if not self.color_sensor_control:
            self.__updateManual()
        else: 
            self.__updateAuto()
            print(self.seen_color)



    def __start(self, run):
        if not self.beforeEveryRun == None:
            self.beforeEveryRun()
        self.__showcaseInProgress(run.run_number)
        
        run.start()

        if not self.afterEveryRun == None:
            self.afterEveryRun()
        self.entered_center = False

        self.__updateNextRun(current_run = run)
        self.__showcaseNextRun()



    def __showcaseInProgress(self, run_number):
        self.telemetry.clear()
        self.telemetry.addData("                          ")
        self.telemetry.addData("                          ")
        self.telemetry.addData("run {0}".format(run_number))
        self.telemetry.addData("  in progress...")
    
    #maybe you can modify the telemetry message :D
    def __showcaseNextRun(self):
        self.telemetry.clear()

        if self.__done():
            self.telemetry.addData("                  ")
            self.telemetry.addData("    DONE    ")
            self.telemetry.addData("     <3         ")

            wait(1000)
            return 0
        
        next_run = self.run_list[self.next_run - 1]

        self.telemetry.addData("                         ")
        self.telemetry.addData("next run: {0}".format(self.next_run))
        self.telemetry.addData("                         ")

        if not self.color_sensor_control:
            if next_run.with_center:
                self.telemetry.addData("Button.CENTER +    ")
            self.telemetry.addData(next_run.button)

        else: self.telemetry.addData(run_colors[next_run.run_number - 1])


    def __done(self):
        done = True

        for run in self.run_list:
            if not run.done():
                done = False
        
        return done


