import threading
import time
import copy

from Chess.src.AI.Evaluator import Evaluator
from Chess.src.AI.Minimax import Minimax

class Computer():

    def __init__(self, compColor):
        self.evaluator = Evaluator()
        self.minimax = Minimax()
        self.compColor = compColor

    def findOptimalMove(self, gs, gameClock, mode):
        #create a thread to run in background
        gs2 = copy.deepcopy(gs)
        thread = threading.Thread(target=self.findOptimalMove2, args=(gs, gs2, gameClock, mode))
        thread.daemon = True
        thread.start()

    def findOptimalMove2(self, gs, gs2, gameClock, mode):
        time.sleep(2)
        #find computer's time
        if self.compColor == "w":
            compTime = gameClock.whiteBaseTime
            compIncrement = gameClock.whiteIncrement
        elif self.compColor == "b":
            compTime = gameClock.blackBaseTime
            compIncrement = gameClock.blackIncrement

        #calculate depth from time
        depth = int(((6 * compIncrement) + compTime) / 5)

        self.minimax.findOptimalMove(gs, gs2, depth, self.evaluator)


