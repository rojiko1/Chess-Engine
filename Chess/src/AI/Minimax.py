import random

class Minimax():

    def __init__(self):
        pass

    def findOptimalMove(self, gs, gs2, depth, evaluator):
        evaluator.evaluatePosition(gs2.board)
        legalMoves = gs2.getLegalMoves()
        index = int(len(legalMoves) * random.random())
        #make move
        gs.moveLog.append(legalMoves[index])