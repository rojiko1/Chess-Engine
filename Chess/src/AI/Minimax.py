class Minimax():

    def __init__(self):
        self.numberOfMovesSearched = 0

    def findOptimalMove(self, gs, gs2, depth, evaluator, compColor):
        if compColor == "w":
            CONSTANT = 1
        elif compColor == "b":
            CONSTANT = -1
        legalMoves = gs2.getLegalMoves()
        if len(legalMoves) > 0:
            if len(legalMoves) == 1:
                gs.moveLog.append(legalMoves[0])
            else:
                evaluation, index = self.recursiveMinimax(gs2, depth, 1, legalMoves, evaluator, CONSTANT, -999.9)
                print("Index:", index)

                #make move
                gs.moveLog.append(legalMoves[index])

        print("Searched", str(self.numberOfMovesSearched), "moves")
        self.numberOfMovesSearched = 0

    def recursiveMinimax(self, gs2, depth, currentDepth, legalMoves, evaluator, CONSTANT, networkWideHigh):
        '''if len(gs2.moveLog) > 0:
            legalMoves = self.reorderLegalMoves(legalMoves, gs2.moveLog[-1])'''
        if depth == currentDepth:
            if currentDepth % 2 == 1:
                CONSTANT2 = 1
            else:
                CONSTANT2 = -1
            highestEval = -999.0
            indexOfHighestEval = -1
            for move in legalMoves:
                gs2.makeMove(move)
                evaluation = CONSTANT * CONSTANT2 * evaluator.evaluatePosition(gs2.board)
                gs2.undoMove()
                self.numberOfMovesSearched += 1
                if evaluation > highestEval:
                    highestEval = evaluation
                    indexOfHighestEval = legalMoves.index(move)
                    if (-1 * highestEval) < networkWideHigh:
                        return -999.0, -1
            return (-1 * highestEval), indexOfHighestEval
        else:
            highestEval = -999.0
            indexOfHighestEval = -1
            for move in legalMoves:
                gs2.makeMove(move)
                legalMoves2 = gs2.getLegalMoves()
                evaluation, index = self.recursiveMinimax(gs2, depth, currentDepth + 1, legalMoves2, evaluator, CONSTANT, highestEval)
                gs2.undoMove()
                if evaluation > highestEval:
                    highestEval = evaluation
                    indexOfHighestEval = legalMoves.index(move)
                    if (-1 * highestEval) < networkWideHigh:
                        return -999.0, -1
            return (-1 * highestEval), indexOfHighestEval

    def reorderLegalMoves(self, legalMoves, lastMove):
        reorderedLegalMoves = []

        #add all capture moves at front of list (recapturing a square as first element)
        for n in range(len(legalMoves) - 1, -1, -1):
            move = legalMoves[n]
            if move.pieceCaptured != "--":
                if (move.endR == lastMove.endR) & (move.endC == lastMove.endC):
                    reorderedLegalMoves.insert(0, move)
                else:
                    reorderedLegalMoves.append(move)
                legalMoves.pop(n)

        #add all non-capture moves
        for move in legalMoves:
            reorderedLegalMoves.append(move)

        return reorderedLegalMoves