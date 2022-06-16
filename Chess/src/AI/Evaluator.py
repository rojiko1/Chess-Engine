class Evaluator():

    def __init__(self):
        self.KING_VALUE = 99.0
        self.QUEEN_VALUE = 9.0
        self.ROOK_VALUE = 5.0
        self.BISHOP_VALUE = 3.0
        self.KNIGHT_VALUE = 3.0
        self.PAWN_VALUE = 1.0

        self.WHITE_KING_MAPPING = [
            [0.03, 0.03, 0.06, 0.06, 0.06, 0.06, 0.03, 0.03],
            [0.03, 0.03, 0.06, 0.06, 0.06, 0.06, 0.03, 0.03],
            [0.06, 0.06, 0.09, 0.09, 0.09, 0.09, 0.06, 0.06],
            [0.06, 0.06, 0.09, 0.12, 0.12, 0.09, 0.06, 0.06],
            [0.06, 0.06, 0.09, 0.15, 0.15, 0.09, 0.06, 0.06],
            [0.09, 0.09, 0.12, 0.15, 0.15, 0.12, 0.09, 0.09],
            [0.24, 0.27, 0.21, 0.18, 0.18, 0.21, 0.27, 0.24],
            [0.51, 0.60, 0.33, 0.24, 0.24, 0.33, 0.60, 0.51]
        ]
        self.BLACK_KING_MAPPING = [
            [0.51, 0.60, 0.33, 0.24, 0.24, 0.33, 0.60, 0.51],
            [0.24, 0.27, 0.21, 0.18, 0.18, 0.21, 0.27, 0.24],
            [0.09, 0.09, 0.12, 0.15, 0.15, 0.12, 0.09, 0.09],
            [0.06, 0.06, 0.09, 0.15, 0.15, 0.09, 0.06, 0.06],
            [0.06, 0.06, 0.09, 0.12, 0.12, 0.09, 0.06, 0.06],
            [0.06, 0.06, 0.09, 0.09, 0.09, 0.09, 0.06, 0.06],
            [0.03, 0.03, 0.06, 0.06, 0.06, 0.06, 0.03, 0.03],
            [0.03, 0.03, 0.06, 0.06, 0.06, 0.06, 0.03, 0.03]
        ]
        self.QUEEN_MAPPING = []
        self.ROOK_MAPPING = [
            [0.13, 0.17, 0.19, 0.22, 0.22, 0.19, 0.17, 0.13],
            [0.11, 0.15, 0.17, 0.20, 0.20, 0.17, 0.15, 0.11],
            [0.05, 0.09, 0.11, 0.14, 0.14, 0.11, 0.09, 0.05],
            [0.03, 0.07, 0.09, 0.12, 0.12, 0.09, 0.07, 0.03],
            [0.03, 0.07, 0.09, 0.12, 0.12, 0.09, 0.07, 0.03],
            [0.05, 0.09, 0.11, 0.14, 0.14, 0.11, 0.09, 0.05],
            [0.11, 0.15, 0.17, 0.20, 0.20, 0.17, 0.15, 0.11],
            [0.13, 0.17, 0.19, 0.22, 0.22, 0.19, 0.17, 0.13]
        ]
        self.BISHOP_MAPPING = [
            [0.24, 0.20, 0.13, 0.08, 0.08, 0.13, 0.20, 0.24],
            [0.20, 0.32, 0.28, 0.21, 0.21, 0.28, 0.32, 0.20],
            [0.13, 0.28, 0.32, 0.28, 0.28, 0.32, 0.28, 0.13],
            [0.08, 0.21, 0.28, 0.32, 0.32, 0.28, 0.21, 0.08],
            [0.08, 0.21, 0.28, 0.32, 0.32, 0.28, 0.21, 0.08],
            [0.13, 0.28, 0.32, 0.28, 0.28, 0.32, 0.28, 0.13],
            [0.20, 0.32, 0.28, 0.21, 0.21, 0.28, 0.32, 0.20],
            [0.24, 0.20, 0.13, 0.08, 0.08, 0.13, 0.20, 0.24]
        ]
        self.KNIGHT_MAPPING = [
            [0.03, 0.05, 0.08, 0.13, 0.13, 0.08, 0.05, 0.03],
            [0.06, 0.14, 0.17, 0.21, 0.21, 0.17, 0.14, 0.06],
            [0.09, 0.17, 0.21, 0.28, 0.28, 0.21, 0.17, 0.09],
            [0.11, 0.21, 0.28, 0.35, 0.35, 0.28, 0.21, 0.11],
            [0.11, 0.21, 0.28, 0.35, 0.35, 0.28, 0.21, 0.11],
            [0.09, 0.17, 0.21, 0.28, 0.28, 0.21, 0.17, 0.09],
            [0.06, 0.14, 0.17, 0.21, 0.21, 0.17, 0.14, 0.06],
            [0.03, 0.05, 0.08, 0.13, 0.13, 0.08, 0.05, 0.03]
        ]
        self.WHITE_PAWN_MAPPING = [
            [0.40, 0.44, 0.34, 0.44, 0.44, 0.44, 0.44, 0.40],
            [0.34, 0.29, 0.33, 0.41, 0.41, 0.35, 0.29, 0.34],
            [0.23, 0.29, 0.31, 0.39, 0.39, 0.37, 0.29, 0.23],
            [0.28, 0.32, 0.34, 0.36, 0.36, 0.35, 0.35, 0.28],
            [0.20, 0.30, 0.33, 0.36, 0.36, 0.33, 0.30, 0.20],
            [0.17, 0.23, 0.31, 0.28, 0.28, 0.31, 0.23, 0.17],
            [0.30, 0.30, 0.25, 0.18, 0.18, 0.25, 0.30, 0.30],
            [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
        ]
        self.BLACK_PAWN_MAPPING = [
            [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
            [0.30, 0.30, 0.25, 0.18, 0.18, 0.25, 0.30, 0.30],
            [0.17, 0.23, 0.31, 0.28, 0.28, 0.31, 0.23, 0.17],
            [0.20, 0.30, 0.33, 0.36, 0.36, 0.33, 0.30, 0.20],
            [0.28, 0.32, 0.34, 0.36, 0.36, 0.35, 0.35, 0.28],
            [0.23, 0.29, 0.31, 0.39, 0.39, 0.37, 0.29, 0.23],
            [0.34, 0.29, 0.33, 0.41, 0.41, 0.35, 0.29, 0.34],
            [0.40, 0.44, 0.34, 0.44, 0.44, 0.44, 0.44, 0.40]
        ]

    def evaluatePosition(self, board, moveNumWhiteCastled, moveNumBlackCastled):
        whiteTotal = 0.0
        blackTotal = 0.0
        for r in range(0, len(board)):
            for c in range(0, len(board[0])):
                piece = board[r][c]
                if piece[0] == "w":
                    if piece[1] == "K":
                        whiteTotal += self.KING_VALUE
                        whiteTotal += self.WHITE_KING_MAPPING[r][c]
                    elif piece[1] == "Q":
                        whiteTotal += self.QUEEN_VALUE
                    elif piece[1] == "R":
                        whiteTotal += self.ROOK_VALUE
                        whiteTotal += self.ROOK_MAPPING[r][c]
                    elif piece[1] == "B":
                        whiteTotal += self.BISHOP_VALUE
                        whiteTotal += self.BISHOP_MAPPING[r][c]
                    elif piece[1] == "N":
                        whiteTotal += self.KNIGHT_VALUE
                        whiteTotal += self.KNIGHT_MAPPING[r][c]
                    elif piece[1] == "p":
                        whiteTotal += self.PAWN_VALUE
                        whiteTotal += self.WHITE_PAWN_MAPPING[r][c]
                elif piece[0] == "b":
                    if piece[1] == "K":
                        blackTotal += self.KING_VALUE
                        blackTotal += self.BLACK_KING_MAPPING[r][c]
                    elif piece[1] == "Q":
                        blackTotal += self.QUEEN_VALUE
                    elif piece[1] == "R":
                        blackTotal += self.ROOK_VALUE
                        blackTotal += self.ROOK_MAPPING[r][c]
                    elif piece[1] == "B":
                        blackTotal += self.BISHOP_VALUE
                        blackTotal += self.BISHOP_MAPPING[r][c]
                    elif piece[1] == "N":
                        blackTotal += self.KNIGHT_VALUE
                        blackTotal += self.KNIGHT_MAPPING[r][c]
                    elif piece[1] == "p":
                        blackTotal += self.PAWN_VALUE
                        blackTotal += self.BLACK_PAWN_MAPPING[r][c]

        if moveNumWhiteCastled > 0: #white castled king side
            whiteTotal += 2.0
        elif moveNumWhiteCastled < 0: #white castled queen side
            whiteTotal += 1.0

        if moveNumBlackCastled > 0: #black castled king side
            blackTotal += 2.0
        elif moveNumBlackCastled < 0: #black castled queen side
            blackTotal += 1.0

        if whiteTotal == blackTotal: #prevent from returning -0.0
            evaluation = 0.0
        else:
            evaluation = round(whiteTotal - blackTotal, 2)
        return evaluation