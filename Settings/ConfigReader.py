from pybricks.parameters import Port, Direction

from Settings.constants import *


class ConfigReader():
    def __init__(self):
        self.config = self.parse_config("Settings//hardware.cfg")

        # Accessing values from the 'Motors' section
        self.left_wheel_port = self.__matchPort(self.config.get('Motors', {}).get('LeftWheelPort'))
        self.right_wheel_port = self.__matchPort(self.config.get('Motors', {}).get('RightWheelPort'))
        self.left_task_port = self.__matchPort(self.config.get('Motors', {}).get('LeftTaskPort'))
        self.right_task_port = self.__matchPort(self.config.get('Motors', {}).get('RightTaskPort'))

        # Accessing values from the 'Sensors' section
        self.gyro_port = self.__matchPort(self.config.get('Sensors', {}).get('GyroPort'))
        self.color_sensor_left_port = self.__matchPort(self.config.get('Sensors', {}).get('ColorSensorLeftPort'))
        self.color_sensor_right_port = self.__matchPort(self.config.get('Sensors', {}).get('ColorSensorRightPort'))
        self.attachment_color_sensor_port = self.__matchPort(self.config.get('Sensors', {}).get('AttachmentColorSensorPort'))

        # Accessing values from the 'Directions' section
        self.left_wheel_direction = self.__matchDirection(self.config.get('Directions', {}).get('LeftWheelDirection'))
        self.right_wheel_direction = self.__matchDirection(self.config.get('Directions', {}).get('RightWheelDirection'))
        self.left_task_direction = self.__matchDirection(self.config.get('Directions', {}).get('LeftTaskDirection'))
        self.right_task_direction = self.__matchDirection(self.config.get('Directions', {}).get('RightTaskDirection'))

        if not self.left_wheel_direction is self.right_wheel_direction:
            # clearly something is wrong
            print("\n\nWheel motors directions should match, but your LEFT is {0} and RIGHT is {1}"
                  .format(self.left_wheel_direction, self.right_wheel_direction))
            print("I'll change both directions to {0} for you. If you did this on purpose, change line 28 in **ConfigReader.py**"
                  .format(self.left_wheel_direction))
            self.right_wheel_direction = self.left_wheel_direction
        
        if self.left_wheel_direction is Direction.CLOCKWISE:
            self.PID_multiplier = 1
        else: self.PID_multiplier = -1





    def parse_config(self, file_path):
        config = {}

        with open(file_path, 'r') as f:
            section = None
            for line in f:
                line = line.strip()
                if not line or line.startswith(';'):  # Skip empty lines and comments
                    continue
                if line.startswith('[') and line.endswith(']'):  # Section header
                    section = line[1:-1]
                    config[section] = {}
                elif '=' in line and section:  # Key-value pair
                    key, value = map(str.strip, line.split('=', 1))
                    config[section][key] = value

        return config



    def __matchPort(self, config_port: str) -> Port:
        if config_port == 'A':
            return Port.A
        if config_port == 'B':
            return Port.B
        if config_port == 'C':
            return Port.C
        if config_port == 'D':
            return Port.D
        
        if config_port == '1':
            return Port.S1
        if config_port == '2':
            return Port.S2
        if config_port == '3':
            return Port.S3
        if config_port == '4':
            return Port.S4

        return None
    
    def __matchDirection(self, config_direction: str) -> Port:
        if config_direction == "CLOCKWISE":
            return Direction.CLOCKWISE
        if config_direction == "COUNTERCLOCKWISE":
            return Direction.COUNTERCLOCKWISE
        
        return None