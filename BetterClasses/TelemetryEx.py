from pybricks.hubs import EV3Brick

# generic class for message showcasing on brick's screen
class TelemetryEx():
    def __init__(self, brick: EV3Brick):
        self.__brick = brick
    
    def addData(self, *message):
        self.__brick.screen.print(message)
    
    def clear(self):
        self.__brick.screen.clear()
