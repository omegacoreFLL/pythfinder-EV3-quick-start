<p align="center" style="margin-bottom: 10px;">
      <img src="https://i.ibb.co/mHSpjdL/pyth-finder-logo-ev3-quickstart.png" alt="pyth-finder-ev3-logo" border="0">
</p>

![version_badge](https://img.shields.io/badge/alpha-0.0.4-006400)
![quickstart](https://img.shields.io/badge/EV3_implementation-006400)
![license](https://img.shields.io/badge/license-MIT-62e39e)


# Installation
## Pybricks
Prior to attempting to utilize our library on a competition EV3 robot, it is crucial that you have a solid understanding of the `MicroPython` software.

If you are new to MicroPython and have not worked with it previously, you need to carefully follow [**THIS INSTALLATION GUIDE**](0) for *`Pybricks`* tailored to your specific devices.


Furthermore, to enable auto-complete features when coding, ensure you install `pybricks`, `pybricksdev`, and `pybricks-stubs` using **pip** in your development environment. If you choose not to use auto-complete, you can adjust the settings by editing the `settings.json` file according to the instructions in the comments.


## PythFinder

To initiate the process of using the quick start guide, you will first need to clone the repository to your local environment. This can be accomplished by carefully following the outlined steps below:

1) Click on the *Code* button from the GitHub page;
2) Copy the project url;

<p align="center">
    <img src="https://i.ibb.co/MphJscW/img1-ev3.png" alt="install-1">
</p>

3) Open Visual Studio code and click on 'Clone Git Repository' on the Welcome page. Alternatively, you can find this button in the **Explorer** tab;

<p align="center">
    <img src="https://i.ibb.co/khMvVjw/img2-ev3.png" alt="install-2">
</p>

4) A window should pop on the top of the screen. Paste the link;
5) Click on 'Clone from URL' button 
(make sure you are connected to your GitHub account);

<p align="center">
    <img src="https://i.ibb.co/JmQ9zZG/img3-ev3.png" alt="install-3">
</p>


6) Select the folder you want to clone the project into

<p align="center">
    <img src="https://i.ibb.co/5MDHYKF/img4-ev3.png" alt="install-4">
</p>

And you're done!! Now you can play with all the features!

<p align="center">
    <img src="https://i.ibb.co/Yk7nvkj/img5-ev3.png" alt="install-5">
</p>


<br/>


# Usage

## Setup
Before you begin using the library, it is essential to customize your specific hardware configuration. This can be achieved by accessing the `hardware.cfg` file located in the **Settings** folder.

<p align="center">
    <img src="https://i.ibb.co/93ZrNbf/img6-ev3.png" alt="setup-1">
</p>

When you open this file, you can modify the `ports` assigned to each *motor* and *sensor*, as well as adjust the direction of the motors to suit YOUR configuration. 

Please be aware that **two wheel motors and a gyro sensor are required** for the library to function properly. The inclusion of additional sensors and motors is *optional*. If you do not have some of these components, simply set their value to `None`.

```ini
# hardware.cfg

[Motors]
LeftWheelPort = C
RightWheelPort = D
LeftTaskPort = B
RightTaskPort = A

[Sensors]
GyroPort = 3
ColorSensorLeftPort = 4
ColorSensorRightPort = 2
AttachmentColorSensorPort = None

[Directions]
LeftWheelDirection = CLOCKWISE
RightWheelDirection = CLOCKWISE
LeftTaskDirection = COUNTERCLOCKWISE
RightTaskDirection = COUNTERCLOCKWISE
```

<br/>

And with that, you'll have **completed** the essential setup!

For those seeking to fine-tune their configuration, additional **advanced settings** can be found in the `constants.py` file. This file contains detailed explanations for each configurable value, with comprehensive comments to guide you through the adjustments.

However, **we strongly recommend** that you still verify the gyro sensor's orientation within the `constants.py` file.

## General Information

### main.py

The `main.py` file serves as the core of the program, housing the **main loop** that drives the entire code.<br/>
When launching the code from the brick's storage, you must execute **THIS** file.


```python
#!/usr/bin/env pybricks-micropython

from RunManager import *

while True:
    core.update()
```

### RunManager.py
The core of the program is managed by the `RunManager.py` file, where you should write **your custom code**.

By default, this file initializes a robot instance and includes methods for a total of **7 runs**.

<p align="center">
    <img src="https://i.ibb.co/bmR7G12/img7-ev3.png" alt="run-manager">
</p>



Within these methods, you can invoke trajectory-following routines or implement external logic. An example 'test' trajectory is already provided and will be automatically executed to demonstrate the setup.

***Using the trajectory data is straightforward***. 

1) Place your text file generated by PythFinder in the **Trajectory/TXT** folder;

<p align="center">
    <img src="https://i.ibb.co/8KYNpNg/img8-ev3.png" alt="trajectory-1">
</p>

2) To create a new trajectory object, start by calling the `.receive()` method and provide the name of the text file as an argument. If your trajectory includes markers, also invoke the `.withMarkers()` method, passing a tuple containing the corresponding methods for each marker in chronological order;

<p align="center">
    <img src="https://i.ibb.co/rF1f5V8/img9-ev3.png" alt="trajectory-2">
</p>

3) Follow the trajectory with the `.follow()` method, passing the robot object as an argument.

<p align="center">
    <img src="https://i.ibb.co/SsD2tbk/img10-ev3.png" alt="trajectory-3">
</p>



While following the trajectory, the robot iterates through all the timestamps from the text file, adjusting the motor powers accordingly.<br/>
This method is **`highly efficient`** as it involves minimal calculations, with the only computation being the heading PID correction.

<br/>

To append a run to each of the buttons, you will need to:
1) Create a reparate function for each of your run programs;

```python
def run1():
    trajectory1.follow(core)

def run2():
    trajectory20.follow(core)
    wait(500)
    trajectory21.follow(core)

def run3():
    ...

...
```

2) Create a run list by instantiating separate `Run()` objects for each of your desired programs. The parameters for each `Run()` instance should be provided in the following order:
    * The **button** that needs to be pressed to initiate the run;
    * The **function** to be executed during the run;
    * A boolean indicating whether the run should be executable **only once or multiple times**;
    * An optional parameter is the **run number**. If no number is specified, the code will automatically assign a number based on the run's position in the list;
    * Another optional parameter to specify if the run should be **combined** with pressing the middle button;

```python
run_list = [Run(Button.UP, function = test, one_time_use =  False, with_center = False),
            Run(Button.LEFT, function = dummy, one_time_use = False, run_number = 2),
            Run(Button.DOWN, function = dummy, one_time_use = False),
            Run(Button.DOWN, function = dummy, one_time_use = False)]
```

If two or more runs share the same button combination for access, they will be executed sequentially according to the run numbers assigned to them.

3) Add the list to the run controller. Failing to do so will result in an error;

```python
core.run_control.addRunList(run_list)
```

4) You can also implement optional *`before_run`* and *`after_run`* methods, as demonstrated in the example below. These methods allow for additional actions to be executed before and after each run, providing greater flexibility and control over the robot's behavior.

```python
core.run_control.addBeforeEveryRun(function = start_run)
core.run_control.addAfterEveryRun(function = stop_run)

```

### TeleOp.py
To facilitate easier testing of the robot's mechanical components, such as the attachments or drivetrain, we have included code that allows you to **control the robot using a game controller**.

This system is compatible with `PS3`, `PS4`, and `most Bluetooth controllers` that can connect to and be recognized by the EV3. It's designed to be plug-and-play, simply run the `TeleOp.py` file instead of `main.py`. For those interested in more advanced customization options, please refer to the **TeleOp.py** file itself.

The control scheme for operating the robot is as follows:

<p align="center">
    <img src="https://i.ibb.co/K7XPnXV/controller-scheme.png" alt="trajectory-3">
</p>

1) Select the **LEFT** task motor (if you have one);
2) Selecte the **RIGHT** task motor (if you have one);
3) Move the robot **FORWARDS** / **BACKWARDS**;
4) **TURN** the robot;
5) **STOP** the selected task motor;
6) set a **POSITIVE** dc power to the selected task motor;
7) set a **NEGATIVE** dc power to the selected task motor;

## Advanced Usage

*Check out the full library [here][1]*


*v. 0.0.4-alpha*



[0]: https://pybricks.com/ev3-micropython/startinstall.html "install pybricks"
[1]: https://github.com/omegacoreFLL/PythFinder
[2]: https://github.com/omegacoreFLL/MasterPiecE/blob/main/TankDrive/constants.py
