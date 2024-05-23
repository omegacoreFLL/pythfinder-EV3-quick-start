# **Installing:**
*outdated photots, but the same essential steps*

First, copy the project url from the GitHub page:

<p align="center">
    <img src="https://i.ibb.co/R6XhyKw/install-1.png" alt="install-1">
</p>

Open Visual Studio code and click on 'Source Control' --> 'Open Repository'

<p align="center">
    <img src="https://i.ibb.co/jvzTcqf/install-2.png" alt="install-2">
</p>

A window should pop on the top of the screen. Paste the link and click on 'Clone Repository' <br>
(make sure you are connected to your GitHub account)

<p align="center">
    <img src="https://i.ibb.co/SXJsmZ6/install-3.png" alt="install-3">
</p>


Select the folder you want to clone the project into

<p align="center">
    <img src="https://i.ibb.co/qJq9hxR/install-4.png" alt="install-4">
</p>

And you're done!! Now you can play with all the features!

<p align="center">
    <img src="https://i.ibb.co/Hr0Phpm/install-5.png" alt="install-5">
</p>



# **Usage:**

## General Information

### main.py
The `main.py` file is the heart of the program. It contains the default `loop()` method, along with some commented-out code that can be useful for determining the loop frequency.
```python
# snippet from 'main.py'

    # delete comments to see the frequency of one full loop
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
In those, you can call trajectory following or external logic.

Reading trajectory data is straightforward. First, place your text file in the **Trajectory/TXT** folder. Then, create a new trajectory object and call the `.receive()` method, passing the name of the text file. If you have markers, also call the `.withMarkers()` method and pass the corresponding methods for each marker as a tuple. To follow the trajectory, call the `.follow()` method and pass the robot object. 

When following the trajectory, the robot loops through all timestamps from the text file and adjusts motor powers accordingly. This approach is **`very fast`** since it requires minimal calculations. The only calculation performed is for the heading PID, which ensures the robot moves straight. Pure feedback control is used only during turns, where the trajectory follower pauses to let the `.turnDeg()` method execute.

Optional '*before_run*' and '*after_run*' methods are also generated for managing LED control (these should not be modified). Next, create a **list** of `Run` objects, specifying at least a **button** and a **function** to be executed.

Finally, add this list to the robot's run controller. Failing to do so will result in an error.
```python
# snippet from 'RunManager.py'

    # create the main robot object here
    core = Robot()

    # build the trajectory
    trajectory = Trajectory().recieve('test')

    ...

    # create functions for each run you want to do
    def run1():
        trajectory.follow(core)
        ...

    # main loop function. Need to be called on loop in 'main.py'
    def loop():
        if core.run_control.entered_center:
            core.led_control.entered_center()
        else: core.led_control.not_started()
        core.update()

    # defining '.start_run()' and '.stop_run()' methods 
    ...

    # create the run list
    run_list = [Run(button = Button.UP, function = run1, one_time_use =  False, with_center = False)]

    core.run_control.addRunList(run_list)

    # optional
    core.run_control.addBeforeEveryRun(function = start_run)
    core.run_control.addAfterEveryRun(function = stop_run)
```

### robot.py
All functionalities of this library are encapsulated in `robot.py`. This file assumes a standard EV3 robot configuration:
* **2 drive motors**
* **2 task motors**
* **2 color sensor (for line following / squaring)**
* **1 gyro**

If you have a different configuration, feel free to modify the code accordingly. Adjust the gyro orientation here to match your hardware setup. For instance, our test robot had the gyro mounted upside down, so we kept the default orientation value.

You can also add sensors or remove task motors as needed. Once all hardware is correctly assigned, your `configuration is complete`.


```python
# snippet from 'main.py'

    # core class, assuming the most common configuration of an ev3 FLL robot:
    #               - 2 driving motors
    #               - 2 free motors (for attachments)
    #               - 2 color sensors, symmetrical to an imaginary middle line, in front of the robot
    #               - 1 gyro sensor
    class Robot:
        def __init__(self):
            self.brick = EV3Brick()

            # modify hardware objects accordingly. Port values will be assigned later, don't worry about it
            self.leftTask = Motor(ltPort, positive_direction = Direction.COUNTERCLOCKWISE)
            self.leftDrive = Motor(ldPort)
            self.leftColor = ColorSensor(lcPort)
    
            self.rightTask = Motor(rtPort, positive_direction = Direction.COUNTERCLOCKWISE)
            self.rightDrive = Motor(rdPort)
            self.rightColor = ColorSensor(rcPort)

            self.gyro = GyroSensor(gyroPort)
            ...
            # set gyro orientation here
            self.localizer = TwoWheelLocalizer(self.leftDrive, self.rightDrive, self.gyro, upside_down_gyro = True)

    ...
```

### constants.py


Default unit measures and necessary constants are listed in the file. You'll primarily be tuning the PID controller for turning. Other values to adjust include color thresholds, booleans, and measurements taken with a ruler or tape measure.

Tuning the `PID controller` can be challenging, so here are the recommended steps:
* Make a dedicated run to just turning;
* Gradually increase kP until the robot reaches the target and possibly oscillates slightly, but avoid aggressive oscillations;
* Slowly increase kD until the oscillations disappear or are significantly reduced;
* kI is generally unnecessary and should be avoided;
* If the position is within a reasonable threshold of the target (approximately 2 degrees), you have successfully tuned the PID!


There are excellent tutorials online for tuning a PID controller. <br/>
If you encounter difficulties, refer to our  [MasterPiece][2] season code,  or reach out to us here or on our social media accounts. We are more than happy to help!

## Advanced Usage

*Check out the full library [here][1]*


*v. 0.0.3-alpha*



[0]: https://pybricks.com/ev3-micropython/startinstall.html "install pybricks"
[1]: https://github.com/omegacoreFLL/PythFinder
[2]: https://github.com/omegacoreFLL/MasterPiecE/blob/main/TankDrive/constants.py