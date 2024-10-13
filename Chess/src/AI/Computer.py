import threading
import time
import copy
import math

from stockfish import Stockfish

from Chess.src.AI.Evaluator import Evaluator
from Chess.src.AI.Minimax import Minimax
from Chess.src.Engine.Move import Move

class Computer():

    def __init__(self, compColor):
        self.evaluator = Evaluator()
        self.minimax = Minimax()
        self.compColor = compColor
        self.stockfish = Stockfish("C:/Users/rkade/Downloads/stockfish-windows-x86-64-avx2/stockfish/stockfish-windows-x86-64-avx2")

    def findOptimalMove(self, gs, gameClock, stockfish=True):
        #create a thread to run in background
        gs2 = copy.deepcopy(gs)
        if stockfish:
            self.stockfish.set_position(gs2.stockfishMoveLog())
            stringMove = self.stockfish.get_best_move()
            sfMove = Move(Move.getSquare(stringMove[:2]), Move.getSquare(stringMove[2:4]), gs.board)
            for move in gs2.getLegalMoves():
                if move == sfMove:
                    gs.moveLog.append(move)
                    return
        else:
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
        #calculate number of pieces
        for r in range(0, len(gs.board)):
            for c in range(0, len(gs.board[0])):
                if gs.board[r][c] != "--":
                    numPieces += 1

        endGameValue = math.pow(1089 - math.pow(numPieces, 2), 1/2) / 8
        return endGameValue