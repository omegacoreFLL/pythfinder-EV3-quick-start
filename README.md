![pyth_finder_logo_mk3](https://github.com/omegacoreFLL/PythFinder/assets/159171107/1dc439b2-0ac0-40f8-95fd-4883b0507603)

# **Installing:**
First, copy the project url from the GitHub page:

![install0](https://github.com/omegacoreFLL/PythFinder/assets/159171107/f92ec725-ea0a-466c-a23b-bc8e0067dc9e)

Open Visual Studio code and click on 'Source Control' --> 'Open Repository'

<p align="center">
    <img src="https://github.com/omegacoreFLL/PythFinder/assets/159171107/aa8d7de3-aee8-41cc-98a4-44bf99402044">
</p>

A window should pop on the top of the screen. Paste the link and click on 'Clone Repository' <br>
(make sure you are connected to your GitHub account)

<p align="center">
    <img src="https://github.com/omegacoreFLL/PythFinder/assets/159171107/359b197b-92bc-4c27-92ab-64ebb9026b25">
</p>


Select the folder you want to clone the project into

![install3](https://github.com/omegacoreFLL/PythFinder/assets/159171107/93a69fb0-421e-403e-a411-1421279aa07e)

And you're done!! Now you can play with all the features!

![install4](https://github.com/omegacoreFLL/PythFinder/assets/159171107/2b99c894-ec84-4809-8e59-796e1ce52da7)

# **Usage:**

## General information

### main.py
The core of your program it's going to be the 'main.py' file, where you have the default loop() method and some commented code, useful for finding the frequency of the loops.
```python
    #delete comments to see the frequency of one full loop
    frequency_timer = StopWatch()
    start_loop_time = 0
    
    while True:
        loop() 

    #end_loop_time = frequency_timer.time()
    #print("Frequency: {:.2f} loops / second".format(1000 / (end_loop_time - start_loop_time)))
    #start_loop_time = end_loop_time
```

### RunManager.py
The actual code is coordinated by 'RunManager.py', the file in which you should write your code.
By default, it creates a robot instance and contains methods for 7 total runs and the main 'loop()'. 
In those, you can use the motion functions defined in *TankDrive/pathing*.

Some optional *before / after every run* methods are also generated for taking care of the led control (you shouldn't modify those).
Then you need to creat a **list** of Run objects, specifying at least a **button** and a **function** to be executed.

In the end, add this list to the robot's run controller. Skipping this step will result into an error.
```python
    #create the main robot object here
    core = Robot()

    ...

    #create functions for each run you want to do
    def run1():
    return 0

    #main loop function. Need to be called on loop in 'main.py'
    def loop():
        if core.run_control.entered_center:
            core.led_control.entered_center()
        else: core.led_control.not_started()
        core.update()

    #defining 'start_run()' and 'stop_run()' methods 
    ...

    #create the run list. See the documentation to understand each parameter
    run_list = [Run(button = Button.UP, function = run1, oneTimeUse =  False, with_center = False)]

    core.run_control.addRunList(run_list)

    #optional
    core.run_control.addBeforeEveryRun(function = start_run)
    core.run_control.addAfterEveryRun(function = stop_run)
```

### robot.py
All functionalities of this library are incapsulated in 'robot.py'. This file assumes a standard EV3 robot configuration: 
* **2 drive motors**
* **2 task motors**
* **2 color sensor (for line following / squaring)**
* **1 gyro**
<a/>
but if you have other configurations, don't hesitate to modify the code acordingly.
Gyro orientation should be changed here to match your hardware. Our test robot had the gyro upside down, remaining the default value.
You can also add sensors and remove task motors.
After making sure all hardware is correctly assigned, you're done configuring here.

```python
    #core class, assuming the most common configuration of an ev3 FLL robot:
    #               - 2 driving motors
    #               - 2 free motors (for attachments)
    #               - 2 color sensors, symmetrical to an imaginary middle line, in front of the robot
    #               - 1 gyro sensor
    class Robot:
        def __init__(self):
            self.brick = EV3Brick()

            #modify hardware objects accordingly. Port values will be assigned later, don't worry about it
            self.leftTask = Motor(ltPort, positive_direction = Direction.COUNTERCLOCKWISE)
            self.leftDrive = Motor(ldPort)
            self.leftColor = ColorSensor(lcPort)
    
            self.rightTask = Motor(rtPort, positive_direction = Direction.COUNTERCLOCKWISE)
            self.rightDrive = Motor(rdPort)
            self.rightColor = ColorSensor(rcPort)

            self.gyro = GyroSensor(gyroPort)
            ...
            #set gyro orientation here
            self.localizer = TwoWheelLocalizer(self.leftDrive, self.rightDrive, self.gyro, upside_down_gyro = True)

    ...
```
