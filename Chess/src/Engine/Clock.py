class Clock():

    def __init__(self, whiteBaseTime, whiteIncrement, blackBaseTime, blackIncrement):
        self.whiteBaseTime = whiteBaseTime * 60
        self.whiteIncrement = whiteIncrement
        self.blackBaseTime = blackBaseTime * 60
        self.blackIncrement = blackIncrement

    def resetClock(self, whiteBaseTime, whiteIncrement, blackBaseTime, blackIncrement):
        self.whiteBaseTime = whiteBaseTime * 60
        self.whiteIncrement = whiteIncrement
        self.blackBaseTime = blackBaseTime * 60
        self.blackIncrement = blackIncrement

    def increment(self, color):
        if color == "w":
            self.whiteBaseTime = self.whiteBaseTime + self.whiteIncrement
        elif color == "b":
            self.blackBaseTime = self.blackBaseTime + self.blackIncrement

    def decrement(self, color):
        if color == "w":
            self.whiteBaseTime = self.whiteBaseTime - self.whiteIncrement
        elif color == "b":
            self.blackBaseTime = self.blackBaseTime - self.blackIncrement

    def updateClock(self, color):
        if color == "w":
            self.whiteBaseTime = self.whiteBaseTime - 1
        elif color == "b":
            self.blackBaseTime = self.blackBaseTime - 1