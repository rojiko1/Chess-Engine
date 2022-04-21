class Evaluator():

    def __init__(self):
        self.KING_VALUE = 99.0
        self.QUEEN_VALUE = 9.0
        self.ROOK_VALUE = 5.0
        self.BISHOP_VALUE = 3.0
        self.KNIGHT_VALUE = 3.0
        self.PAWN_VALUE = 1.0

    def evaluatePosition(self, board):
        whiteTotal = 0
        blackTotal = 0
        for r in range(0, len(board)):
            for c in range(0, len(board[0])):
                piece = board[r][c]
                if piece[0] == "w":
                    if piece[1] == "K":
                        whiteTotal += self.KING_VALUE
                    elif piece[1] == "Q":
                        whiteTotal += self.QUEEN_VALUE
                    elif piece[1] == "R":
                        whiteTotal += self.ROOK_VALUE
                    elif piece[1] == "B":
                        whiteTotal += self.BISHOP_VALUE
                    elif piece[1] == "N":
                        whiteTotal += self.KNIGHT_VALUE
                    elif piece[1] == "p":
                        whiteTotal += self.PAWN_VALUE
                elif piece[0] == "b":
                    if piece[1] == "K":
                        blackTotal += self.KING_VALUE
                    elif piece[1] == "Q":
                        blackTotal += self.QUEEN_VALUE
                    elif piece[1] == "R":
                        blackTotal += self.ROOK_VALUE
                    elif piece[1] == "B":
                        blackTotal += self.BISHOP_VALUE
                    elif piece[1] == "N":
                        blackTotal += self.KNIGHT_VALUE
                    elif piece[1] == "p":
                        blackTotal += self.PAWN_VALUE

        evaluation = whiteTotal - blackTotal
        print("Computer evaluation is: " + str(evaluation))
        return evaluation
