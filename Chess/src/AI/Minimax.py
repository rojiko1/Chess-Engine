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
            if len(legalMoves) == 1: #if only one possible move, make move
                gs.moveLog.append(legalMoves[0])
            else:
                #copyLegalMoves = copy.deepcopy(legalMoves)
                evaluation, move = self.recursiveMinimax(gs2, depth, 1, legalMoves, evaluator, CONSTANT, -999.0)

                #make move
                gs.moveLog.append(move)

        print("Searched", str(self.numberOfMovesSearched), "moves")
        self.numberOfMovesSearched = 0

    def recursiveMinimax(self, gs2, depth, currentDepth, legalMoves, evaluator, CONSTANT, networkWideHigh):
        #move all the way down to the depth specified
        #for each possible outcome, evaluate board
        #best evaluation for the color whose move it is gets passed up that branch
        #repeat process until reaching the root node
        #return the evaluation and index of the best move
        if len(gs2.moveLog) > 0:
            legalMoves = self.reorderLegalMoves(legalMoves, gs2.moveLog[-1]) #reorder moves so that more can be pruned (reduce time complexity)
        if depth == currentDepth:
            if currentDepth % 2 == 1:
                CONSTANT2 = 1
            else:
                CONSTANT2 = -1
            highestEval = -999.0
            # indexOfHighestEval = -1
            bestMove = None
            if len(legalMoves) > 0:
                for move in legalMoves:
                    gs2.makeMove(move)
                    evaluation = CONSTANT * CONSTANT2 * evaluator.evaluatePosition(gs2.board, gs2.moveNumWhiteCastled, gs2.moveNumBlackCastled)
                    gs2.undoMove()
                    self.numberOfMovesSearched += 1
                    if evaluation > highestEval:
                        highestEval = evaluation
                        # indexOfHighestEval = legalMoves.index(move)
                        bestMove = move
                        if (-1 * highestEval) < networkWideHigh:
                            return -999.0, -1
            elif gs2.inCheck(gs2.getTurnColor()):
                return 999.0, None
            else:
                return 0.0, None
            return (-1 * highestEval), bestMove
        else:
            highestEval = -999.0
            # indexOfHighestEval = -1
            bestMove = None
            if len(legalMoves) > 0:
                for move in legalMoves:
                    gs2.makeMove(move)
                    legalMoves2 = gs2.getLegalMoves()
                    evaluation, oppMove = self.recursiveMinimax(gs2, depth, currentDepth + 1, legalMoves2, evaluator, CONSTANT, highestEval)
                    gs2.undoMove()
                    if evaluation > highestEval:
                        highestEval = evaluation
                        # indexOfHighestEval = legalMoves.index(move)
                        bestMove = move
                        if (-1 * highestEval) < networkWideHigh:
                            return -999.0, -1
            elif gs2.inCheck(gs2.getTurnColor()):
                return 999.0, None
            else:
                return 0.0, None
            return (-1 * highestEval), bestMove

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