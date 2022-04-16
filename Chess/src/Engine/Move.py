class Move():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {i: j for j, i in ranksToRows.items()}
    filesToColumns = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    columnsToFiles = {i: j for j, i in filesToColumns.items()}

    def __init__(self, startSq, endSq, board, enPassant = False, castling = False):
        self.startR = int(startSq[0])
        self.startC = int(startSq[1])
        self.endR = int(endSq[0])
        self.endC = int(endSq[1])
        self.pieceMoved = board[self.startR][self.startC]
        self.pieceCaptured = board[self.endR][self.endC]
        self.moveID = self.startR * 1000 + self.startC * 100 + self.endR * 10 + self.endC
        #pawn promotion
        self.pawnPromotion = (self.pieceMoved[1] == "p") & (((self.pieceMoved[0] == "w") & (self.endR == 0)) | ((self.pieceMoved[0] == "b") & (self.endR == 7)))
        self.promotionChoice = "Q"
        #en passant
        self.enPassant = enPassant
        #castling
        self.castling = castling

        self.notation = ""

    def __eq__(self, other):
        if isinstance(other, Move):
            if self.moveID == other.moveID:
                return True
            else:
                return False

    def generateChessNotation(self, gs):
        notation = ""
        if self.pieceMoved[1] == "K":
            notation = "K" + self.getRankFile(self.endR, self.endC)
        elif self.pieceMoved[1] == "Q":
            notation = "Q" + self.getRankFile(self.endR, self.endC)
        elif self.pieceMoved[1] == "R":
            notation = "R" + self.getRankFile(self.endR, self.endC)
        elif self.pieceMoved[1] == "B":
            notation = "B" + self.getRankFile(self.endR, self.endC)
        elif self.pieceMoved[1] == "N":
            notation = "N" + self.getRankFile(self.endR, self.endC)
        elif self.pieceMoved[1] == "p":
            notation = self.getRankFile(self.endR, self.endC)

        if not self.pieceCaptured == "--":
            p1 = notation[:-2]
            p2 = notation[-2:]
            notation = p1 + "x" + p2
            if notation[0] == "x":
                notation = self.getRankFile(self.startR, self.startC)[0] + notation

        if self.pawnPromotion:
            notation = notation + "=" + self.promotionChoice

        if self.castling:
            if self.endC == 2:
                notation = "O-O-O"
            elif self.endC == 6:
                notation = "O-O"

        if gs.inCheck(gs.getOppColor(self.pieceMoved[0])):
            notation = notation + "+"

        self.notation = notation

    def updateNotationWithCheckmate(self):
        self.notation = self.notation[:-1] + "#"

    def getRankFile(self, r, c):
        return self.columnsToFiles[c] + self.rowsToRanks[r]