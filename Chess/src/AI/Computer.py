import threading
import time
import copy
import math

from Chess.src.AI.Evaluator import Evaluator
from Chess.src.AI.Minimax import Minimax

class Computer():

    def __init__(self, compColor):
        self.evaluator = Evaluator()
        self.minimax = Minimax()
        self.compColor = compColor

    def findOptimalMove(self, gs, gameClock):
        #create a thread to run in background
        gs2 = copy.deepcopy(gs)
        thread = threading.Thread(target=self.findOptimalMove2, args=(gs, gs2, gameClock))
        thread.daemon = True
        thread.start()

    def findOptimalMove2(self, gs, gs2, gameClock):
        begin = time.time()

        #find computer's time
        if self.compColor == "w":
            compTime = gameClock.whiteBaseTime
            compIncrement = gameClock.whiteIncrement
        elif self.compColor == "b":
            compTime = gameClock.blackBaseTime
            compIncrement = gameClock.blackIncrement

        #calculate depth from time and endgame value
        depth = round(math.pow((((6 * compIncrement) + compTime) / 10000), 1/4) * math.pow(self.calculateEndGameValue(gs), 1/2))

        self.minimax.findOptimalMove(gs, gs2, depth, self.evaluator, self.compColor)

        end = time.time()

        print("Time elapsed:", str(round((end - begin) * 1000)), "ms")

    def calculateEndGameValue(self, gs):
        numPieces = 0
        for r in range(0, len(gs.board)):
            for c in range(0, len(gs.board[0])):
                if gs.board[r][c] != "--":
                    numPieces += 1

        endGameValue = math.pow(1089 - math.pow(numPieces, 2), 1/2) / 8
        return endGameValue


