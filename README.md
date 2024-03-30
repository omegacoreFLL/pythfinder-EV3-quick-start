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

## General Information

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
In those, you can use the motion functions defined in *TankDrive/pathing.py*.

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

### pathing.py

In *TankDrive/pathing.py* you'll see all motion methods, and be able to modify or create new and improved ones.
These functions use feedback + feedforward control for positioning, using different constants for different scenarios.
You are able to chain them to achieve much smoother and complex pathing, without the need of complex planning (because the brick can't take it).
One example is found in the 'test()' method from 'RunManager.py'. 
The main parameters here are the target (heading / Pose) and robot instance.

The field coordinate system assumes that **+X** is in the front of the robot, **+Y** in the right and positive **rotation** is clockwise.

If you're a beginner team, don't modify this file at all.

```python
    ...

    #function for going a certain distance ('cm' and 'robot' values are the only mandatory ones)
    def inLineCM(cm, robot, inOtherFunction = False,
            threshold = 0.1, 
            sensitivity = 1, 
            correctHeading = True, tangential_angle = None,
            interpolating = False, accelerating = False,
            listOfCommands = None):
    ...

```

### constants.py

Here you'll spend most of the time configuring values ('TankDrive/constants.py').

Default unit measures are listed in the file, so are the constants you need / don't need to change.
You'll mostly tune the PID and kS gains for turning and driving a certain distance.
Some other values will be color thresholds, booleans and measured values (with a ruler or measure tape).

Tunning the PID should be the hardest part, both for turning and driving, so here are the recommended steps:
* make a dedicated run to just one movement (turnDeg, inLineCM etc.).
* increase the kP until it reaches the target, and even oscillates a bit, but don't increase it to a point the robot oscillates aggressively (excepting for the aggressive constants).
* slowly increase kD, untill the oscilations dissapear, or at least reduce.
* don't really work with kI, you don't need it.
* if the position in within a reasonable threshold to the target (~2 deg / ~2-3 cm), you did it!
<a/>

There are good tutorials online on how to tune a PID controller. <br>
If you can't get it right, look into our [MasterPiece](https://github.com/omegacoreFLL/MasterPiecE/blob/main/TankDrive/constants.py) season code, or just write us here or on our social media accounts. We are more than happy to help!

## Advanced Usage

Check out the documentation. --- **TO BE ADDED**


*v. alpha1.0.0*
