class Clock():

    def __init__(self, baseTime, incrementTime):
        self.whiteBaseTime = baseTime * 60
        self.whiteIncrement = incrementTime
        self.blackBaseTime = baseTime * 60
        self.blackIncrement = incrementTime

        if baseTime < 3:
            self.lowTimeThreshold = 10
        elif baseTime < 10:
            self.lowTimeThreshold = 30
        elif baseTime < 30:
            self.lowTimeThreshold = 60
        else:
            self.lowTimeThreshold = 120

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