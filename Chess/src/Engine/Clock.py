import pygame as p
import threading
import time

class Clock():

    def __init__(self, baseTime, incrementTime, gameType):
        #measured in milliseconds
        self.whiteBaseTime = baseTime * 60 * 1000
        self.whiteIncrement = incrementTime * 1000
        self.blackBaseTime = baseTime * 60 * 1000
        self.blackIncrement = incrementTime * 1000

        self.gsReference = None
        self.gameType = gameType

        if baseTime < 3:
            self.lowTimeThreshold = 10 * 1000
        elif baseTime < 10:
            self.lowTimeThreshold = 30 * 1000
        elif baseTime < 30:
            self.lowTimeThreshold = 60 * 1000
        else:
            self.lowTimeThreshold = 120 * 1000

    def resetClock(self, whiteBaseTime, whiteIncrement, blackBaseTime, blackIncrement):
        self.whiteBaseTime = whiteBaseTime * 60 * 1000
        self.whiteIncrement = whiteIncrement * 1000
        self.blackBaseTime = blackBaseTime * 60 * 1000
        self.blackIncrement = blackIncrement * 1000

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

    def runClock(self, gs):
        p.init()
        self.gsReference = gs
        tickClock = p.time.Clock()
        FPS = 60
        thread = threading.Thread(target=self.runClock2, args=(tickClock, FPS))
        thread.daemon = True
        thread.start()

    def runClock2(self, tickClock, FPS):
        while not self.gsReference.gameOver:
            if len(self.gsReference.moveLog) > 0:
                if self.gsReference.whiteToMove:
                    self.whiteBaseTime = self.whiteBaseTime - (1000 * (time.time() - lastTime))
                else:
                    self.blackBaseTime = self.blackBaseTime - (1000 * (time.time() - lastTime))
            lastTime = time.time()
            tickClock.tick(FPS)

    def updateGSReference(self, gs):
        self.gsReference = gs
