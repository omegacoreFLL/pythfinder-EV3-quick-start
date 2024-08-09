from BetterClasses.EdgeDetectorEx import *
from BetterClasses.ColorSensorEx import *
from BetterClasses.TelemetryEx import *
from BetterClasses.ButtonsEx import *

from Settings.constants import *

# class to describe run-specific constants
class Run():
    def __init__(self, button: Button, 
                       function: function, 
                       run_number: int | None = None, 
                       color: Color | None = None, 
                       one_time_use: bool = True, 
                       with_center: bool = False):
        if not button == None:
            if button == Button.CENTER:
                raise Exception("can't use 'Button.CENTER' for starting a run")
            
        self.button = button
        self.run_number = run_number
        self.runs = 0
        self.one_time_use = one_time_use
        self.with_center = with_center

        self.running = EdgeDetectorEx()

        self.function = function
        self.color = color
        
    
    def hasJustStarted(self):
        return self.running.rising
    
    def hasNotStarted(self):
        return not self.running.rising
    
    def runable(self):
        return not self.one_time_use or not self.runs > 0
    
    def update(self):
        self.running.update()
    
    def start(self):
        if self.hasJustStarted():
            self.runs +=1
            self.function()
            
        self.running.set(False)
        self.running.update()
    
    def done(self):
        return self.one_time_use and self.runs > 0

# logic for run-selection. Don't modify things here    
class RunController():
    def __init__(self, gamepad: ButtonEx, 
                       brick: EV3Brick, 
                       telemetry: TelemetryEx, 
                       run_list = None):

        self.next_run = 1
        self.run_loops = 0
        self.all_one_time_use = True

        self.run_list = run_list
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
        self.after_every_run = None
    


    def addRunList(self, run_list):
        self.run_list = run_list
        self.total_runs = len(self.run_list)

        # number each run in order of the elements in the list
        # + check if program is finite (all runs are one time use)
        for run in range(self.total_runs):
            self.run_list[run].run_number = run + 1

            if not self.run_list[run].one_time_use:
                self.all_one_time_use = False
        
        self.__showcaseNextRun()
    
    def addBeforeEveryRun(self, function: function):
        self.before_every_run = function
    
    def addAfterEveryRun(self, function: function):
        self.after_every_run = function

    def addColorSensor(self, sensor: ColorSensorEx):
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
    


    def __updateManual(self):
        if self.gamepad.wasJustPressed(Button.CENTER):
            self.entered_center = not self.entered_center

        # if more runs have the same button, run the one used fewer times

        # create empty first run
        optimal_run = Run(None, None) 
        optimal_run.runs = -1
        past_run_index = -1

        for run in range(self.total_runs):
            current_run = self.run_list[run]

            # get eligible runnable runs
            if not do_runs_in_order or current_run.run_number == self.next_run:
                self.__shouldStartRun(current_run)

                if current_run.hasJustStarted():

                    if optimal_run.button == None:
                        optimal_run = current_run
                        past_run_index = run

                    # this is the case of runs accessed through the same button
                    elif current_run.runs < optimal_run.runs:
                        self.run_list[past_run_index].running.set(False)
                        optimal_run = current_run

                    else: self.run_list[run].running.set(False)

        # found the next run
        if not optimal_run.button == None:          
            self.__start(optimal_run)
        
    def __updateNextRun(self, current_run: Run):
        if not current_run.run_number == self.next_run:
            return None

        verified = 0
        found = False

        # loop through all runs, starting from the one just ran
        # stop when:
        #       - one runnable function is found
        #       - you've looped one time through all runs and you didn't find any runnable one

        while not found and verified <= self.total_runs:

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
        # skip the update when done
        if self.__done():
            return 0
        
        self.gamepad.updateButtons()
        
        if not self.color_sensor_control:
            self.__updateManual()
        else: self.__updateAuto()




    def __shouldStartRun(self, run: Run):
        if not run.runable():
            return None
        
        run.update()

        if (run.with_center and self.entered_center) or (not run.with_center and not self.entered_center):
            if self.gamepad.wasJustPressed(run.button):
                run.running.set(True)

    def __start(self, run: Run):
        if not self.before_every_run == None:
            self.before_every_run()
        self.__showcaseInProgress(run.run_number)
        
        run.start()

        if not self.after_every_run == None:
            self.after_every_run()
        self.entered_center = False

        self.__updateNextRun(current_run = run)
        self.__showcaseNextRun()

    def __done(self):
        for run in self.run_list:
            if not run.done():
                return False
        
        return True




    def __showcaseInProgress(self, run_number: int):
        self.telemetry.clear()
        self.telemetry.addData("                          ")
        self.telemetry.addData("                          ")
        self.telemetry.addData("run {0}".format(run_number))
        self.telemetry.addData("  in progress...")
    
    def __showcaseNextRun(self):
        self.telemetry.clear()

        if self.__done():
            self.telemetry.addData("                  ")
            self.telemetry.addData("    DONE    ")
            self.telemetry.addData("     <3         ")

            return None
        
        next_run = self.run_list[self.next_run - 1]

        self.telemetry.addData("                         ")
        self.telemetry.addData("next run: {0}".format(self.next_run))
        self.telemetry.addData("                         ")

        if not self.color_sensor_control:
            if next_run.with_center:
                self.telemetry.addData("Button.CENTER +    ")
            self.telemetry.addData(next_run.button)

        else: self.telemetry.addData(run_colors[next_run.run_number - 1])



