import copy

class GameState():

    def __init__(self):
        #first letter - black or white
        #second letter - piece type
        #"--" = empty space
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        #initialize king locations
        self.wKingLocation = None
        self.bKingLocation = None
        for r in range(0, len(self.board)):
            for c in range(0, len(self.board[0])):
                if self.board[r][c] == "wK":
                    self.wKingLocation = (r, c)
                elif self.board[r][c] == "bK":
                    self.bKingLocation = (r, c)
        self.checkmate = False
        self.stalemate = False
        self.fiftyMoveRuleDraw = False
        self.drawByRepetition = False
        self.insufficientMaterial = self.checkInsufficentMaterial()
        #initialize right to castle
        self.hasCastlingRight = {'wks': False, 'wqs': False, 'bks': False, 'bqs': False}
        self.castlingRightLost = {'wks': 0, 'wqs': 0, 'bks': 0, 'bqs': 0}
        if self.wKingLocation == (7, 4):
            if self.board[7][7] == "wR":
                self.hasCastlingRight['wks'] = True
                self.castlingRightLost['wks'] = -1
            elif self.board[7][0] == "wR":
                self.hasCastlingRight['wqs'] = True
                self.castlingRightLost['wqs'] = -1
        elif self.bKingLocation == (0, 4):
            if self.board[0][7] == "bR":
                self.hasCastlingRight['bks'] = True
                self.castlingRightLost['bks'] = -1
            elif self.board[0][0] == "bR":
                self.hasCastlingRight['bqs'] = True
                self.castlingRightLost['bqs'] = -1
        self.noCaptureCount = 0
        self.whiteBoards = [[copy.deepcopy(self.board), 1]]
        self.blackBoards = []

    def getTurnColor(self):
        if self.whiteToMove:
            return "w"
        else:
            return "b"

    def getOppColor(self, color):
        if color == "w":
            return "b"
        else:
            return "w"

    def isOnBoard(self, r, c):
        if (r < 0) | (r > 7) | (c < 0) | (c > 7):
            return False
        else:
            return True

    def makeMove(self, move):
        self.board[move.startR][move.startC] = "--"
        color = move.pieceMoved[0]
        if move.pawnPromotion:
            self.board[move.endR][move.endC] = (move.pieceMoved[0] + move.promotionChoice)
        if not move.pawnPromotion:
            self.board[move.endR][move.endC] = move.pieceMoved
        if move.enPassant:
            if color == "w":
                self.board[move.endR + 1][move.endC] = "--"
            elif color == "b":
                self.board[move.endR - 1][move.endC] = "--"
        if move.castling:
            if move.endC == 2:
                self.board[move.endR][0] = "--"
                self.board[move.endR][move.endC + 1] = color + "R"
            elif move.endC == 6:
                self.board[move.endR][7] = "--"
                self.board[move.endR][move.endC - 1] = color + "R"
        if move.pieceCaptured == "--":
            self.noCaptureCount = self.noCaptureCount + 1
        else:
            self.noCaptureCount = 0
        self.moveLog.append(move)
        if self.noCaptureCount >= 50:
            pawnMoveCount = 0
            for index in range(1, 51):
                if self.moveLog[-1 * index].pieceMoved[1] == "p":
                    pawnMoveCount = pawnMoveCount + 1
            if pawnMoveCount == 0:
                self.fiftyMoveRuleDraw = True
        self.recordBoard()
        if self.checkDrawByRepetition():
            self.drawByRepetition = True
        if self.checkInsufficentMaterial():
            self.insufficientMaterial = True
        move.generateChessNotation(self)
        self.updateCastling()
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.wKingLocation = (move.endR, move.endC)
        elif move.pieceMoved == "bK":
            self.bKingLocation = (move.endR, move.endC)

    def updateCastling(self):
        lastMove = self.moveLog[-1]
        color = lastMove.pieceMoved[0]
        pieceType = lastMove.pieceMoved[1]
        if (pieceType == "K") | (lastMove.castling):
            self.updateKingSideCastling(color)
            self.updateQueenSideCastling(color)
        if pieceType == "R":
            if color == "w":
                row = 7
            if color == "b":
                row = 0
            if (lastMove.startR == row) & (lastMove.startC == 0):
                self.updateQueenSideCastling(color)
            if (lastMove.startR == row) & (lastMove.startC == 7):
                self.updateKingSideCastling(color)

    def updateKingSideCastling(self, color):
        if self.castlingRightLost[color + "ks"] < 0:
            self.hasCastlingRight[color + "ks"] = False
            self.castlingRightLost[color + "ks"] = len(self.moveLog)

    def updateQueenSideCastling(self, color):
        if self.castlingRightLost[color + "qs"] < 0:
            self.hasCastlingRight[color + "qs"] = False
            self.castlingRightLost[color + "qs"] = len(self.moveLog)

    def undoMove(self):
        if len(self.moveLog) > 0:
            move = self.moveLog[-1]
            color = move.pieceMoved[0]
            self.deleteBoard()
            self.board[move.startR][move.startC] = move.pieceMoved
            self.board[move.endR][move.endC] = move.pieceCaptured
            if move.enPassant:
                if color == "w":
                    self.board[move.endR + 1][move.endC] = "bp"
                elif color == "b":
                    self.board[move.endR - 1][move.endC] = "wp"
            if move.castling:
                if move.endC == 6:
                    self.board[move.endR][move.endC - 1] = "--"
                    self.board[move.startR][7] = color + "R"
                elif move.endC == 2:
                    self.board[move.endR][move.endC + 1] = "--"
                    self.board[move.startR][0] = color + "R"
            for key, value in self.castlingRightLost.items():
                if value == len(self.moveLog):
                    self.hasCastlingRight[key] = True
                    self.castlingRightLost[key] = -1
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.wKingLocation = (move.startR, move.startC)
            elif move.pieceMoved == "bK":
                self.bKingLocation = (move.startR, move.startC)
            self.moveLog.pop(-1)
            if move.pieceCaptured == "--":
                self.noCaptureCount = self.noCaptureCount - 1
            else:
                self.noCaptureCount = self.findNoCaptureCount()
            self.checkmate = False
            self.stalemate = False
            self.fiftyMoveRuleDraw = False
            self.drawByRepetition = False
            self.insufficientMaterial = False

    def getLegalMoves(self): #considers checks from movement
        turn = self.getTurnColor()
        possibleMoves = self.getPossibleMoves(turn)
        if not self.inCheck(turn):
            if turn == "w":
                location = self.wKingLocation
            elif turn == "b":
                location = self.bKingLocation
            self.getKSCastlingMoves(location[0], location[1], turn, possibleMoves)
            self.getQSCastlingMoves(location[0], location[1], turn, possibleMoves)
        for i in range(len(possibleMoves) - 1, -1, -1):
            self.makeMove(possibleMoves[i])
            if self.inCheck(turn):
                possibleMoves.pop(i)
            self.undoMove()
        if len(possibleMoves) == 0:
            if self.inCheck(turn):
                self.checkmate = True
                self.moveLog[-1].updateNotationWithCheckmate()
            else:
                self.stalemate = True
        return possibleMoves

    def getPossibleMoves(self, color): #does not consider checks from movement
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                piece = self.board[r][c][1]
                if turn == color:
                    if piece == "p":
                        self.getPawnMoves(r, c, color, moves)
                    elif piece == "B":
                        self.getBishopMoves(r, c, color, moves)
                    elif piece == "N":
                        self.getKnightMoves(r, c, color, moves)
                    elif piece == "R":
                        self.getRookMoves(r, c, color, moves)
                    elif piece == "Q":
                        self.getQueenMoves(r, c, color, moves)
                    elif piece == "K":
                        self.getKingMoves(r, c, color, moves)
        return moves

    def inCheck(self, turn):
        if turn == "w":
            return self.squareUnderAttack(self.wKingLocation[0], self.wKingLocation[1], turn)
        elif turn == "b":
            return self.squareUnderAttack(self.bKingLocation[0], self.bKingLocation[1], turn)

    def findNoCaptureCount(self):
        index = 1
        noCaptureCount = 0
        while (index < len(self.moveLog)) & (self.moveLog[-1 * index].pieceCaptured == "--"):
            noCaptureCount = noCaptureCount + 1
            index = index + 1
        return noCaptureCount

    def boardEquals(self, board):
        for r in range(len(board)):
            for c in range(len(board[0])):
                if self.board[r][c] != board[r][c]:
                    return False
        return True

    def recordBoard(self):
        if self.getOppColor(self.getTurnColor()) == "w":
            for board in self.whiteBoards:
                if self.boardEquals(board[0]):
                    board[1] = board[1] + 1
                    return None
            self.whiteBoards.append([copy.deepcopy(self.board), 1])
            return None
        elif self.getOppColor(self.getTurnColor()) == "b":
            for board in self.blackBoards:
                if self.boardEquals(board[0]):
                    board[1] = board[1] + 1
                    return None
            self.blackBoards.append([copy.deepcopy(self.board), 1])
            return None

    def deleteBoard(self):
        if self.getTurnColor() == "w":
            for board in self.whiteBoards:
                if self.boardEquals(board[0]):
                    if board[1] == 1:
                        self.whiteBoards.remove(board)
                    else:
                        board[1] = board[1] - 1
        elif self.getTurnColor() == "b":
            for board in self.blackBoards:
                if self.boardEquals(board[0]):
                    if board[1] == 1:
                        self.blackBoards.remove(board)
                    else:
                        board[1] = board[1] - 1

    def checkDrawByRepetition(self):
        if self.getOppColor(self.getTurnColor()) == "w":
            for board in self.whiteBoards:
                if board[1] == 3:
                    return True
            return False
        elif self.getOppColor(self.getTurnColor()) == "b":
            for board in self.blackBoards:
                if board[1] == 3:
                    return True
            return False

    def checkInsufficentMaterial(self):
        boardPieceCount = {"--": 0, "bp": 0, "bR": 0, "bN": 0, "bB": 0, "bQ": 0, "bK": 0, "wp": 0, "wR": 0, "wN": 0, "wB": 0, "wQ": 0, "wK": 0}
        bishopLocations = []
        for r in range(0, len(self.board)):
            for c in range(0, len(self.board[0])):
                boardPieceCount[str(self.board[r][c])] = boardPieceCount[str(self.board[r][c])] + 1
                if self.board[r][c][1] == "B":
                    bishopLocations.append((r, c))
        if (boardPieceCount["wp"] == 0) & (boardPieceCount["wR"] == 0) & (boardPieceCount["wQ"] == 0) & (boardPieceCount["bp"] == 0) & (boardPieceCount["bR"] == 0) & (boardPieceCount["bQ"] == 0):
            if (boardPieceCount["wN"] == 0) & (boardPieceCount["wB"] == 0) & (boardPieceCount["bN"] == 0) & (boardPieceCount["bB"] == 0):
                return True
            elif ((boardPieceCount["wN"] == 0) & (boardPieceCount["bN"] == 0)) & (((boardPieceCount["wB"] == 1) & (boardPieceCount["bB"] == 0)) | ((boardPieceCount["wB"] == 0) & (boardPieceCount["bB"] == 1))):
                return True
            elif ((boardPieceCount["wB"] == 0) & (boardPieceCount["bB"] == 0)) & (((boardPieceCount["wN"] == 1) & (boardPieceCount["bN"] == 0)) | ((boardPieceCount["wN"] == 0) & (boardPieceCount["bN"] == 1))):
                return True
            elif (boardPieceCount["wB"] == 1) & (boardPieceCount["bB"] == 1) & (len(bishopLocations) == 2):
                firstBishopMoveModulo = (bishopLocations[0][0] + bishopLocations[0][1]) % 2
                secondBishopMoveModulo = (bishopLocations[1][0] + bishopLocations[1][1]) % 2
                if firstBishopMoveModulo == secondBishopMoveModulo:
                    return True
        return False

    def squareUnderAttack(self, r, c, turn):
        oppMoves = self.getPossibleMoves(self.getOppColor(turn))
        for move in oppMoves:
            if (move.endR == r) & (move.endC == c):
                return True
        return False

    def getPawnMoves(self, r, c, color, moves):
        if color == "w":
            if self.board[r-1][c] == "--": #move up one square
               moves.append(Move((r, c), (r-1, c), self.board))
               if r == 6:
                    if self.board[r-2][c] == "--": #move up two squares
                        moves.append(Move((r, c), (r-2, c), self.board))
            if (c-1 >= 0):
                if (self.board[r-1][c-1][0] == "b"): #diagonal left capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if (c+1 <= 7):
                if (self.board[r-1][c+1][0] == "b"): #diagonal right capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))
            if (r == 3) & (len(self.moveLog) > 0):
                if (self.moveLog[-1].startR == 1) & (self.moveLog[-1].endR == r):
                    if self.isOnBoard(r, c-1):
                        if (self.board[r][c-1] == "bp") & (self.moveLog[-1].startC == c-1) & (self.moveLog[-1].endC == c-1):
                            moves.append(Move((r, c), (r-1, c-1), self.board, enPassant = True)) #en passant left
                    if self.isOnBoard(r, c-1):
                        if (self.board[r][c+1] == "bp") & (self.moveLog[-1].startC == c+1) & (self.moveLog[-1].endC == c+1):
                            moves.append(Move((r, c), (r-1, c+1), self.board, enPassant = True)) #en passant right
        elif color == "b":
            if self.board[r+1][c] == "--": #move up one square
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1:
                    if self.board[r+2][c] == "--": #move up two squares
                        moves.append(Move((r, c), (r+2, c), self.board))
            if (c-1 >= 0):
                if (self.board[r+1][c-1][0] == "w"): #diagonal left capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if (c+1 <= 7):
                if (self.board[r+1][c+1][0] == "w"): #diagonal right capture
                    moves.append(Move((r, c), (r+1, c+1), self.board))
            if (r == 4):
                if (self.moveLog[-1].startR == 6) & (self.moveLog[-1].endR == r):
                    if self.isOnBoard(r, c-1):
                        if (self.board[r][c-1] == "wp") & (self.moveLog[-1].startC == c-1) & (self.moveLog[-1].endC == c-1):
                            moves.append(Move((r, c), (r+1, c-1), self.board, enPassant = True)) #en passant left
                    if self.isOnBoard(r, c+1):
                        if (self.board[r][c+1] == "wp") & (self.moveLog[-1].startC == c+1) & (self.moveLog[-1].endC == c+1):
                            moves.append(Move((r, c), (r+1, c+1), self.board, enPassant = True)) #en passant right

    def getBishopMoves(self, r, c, color, moves):
        bishopMoves = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for j in range(0, len(bishopMoves)):
            for i in range(1, 8):
                if not self.isOnBoard(r + (i * bishopMoves[j][0]), c + (i * bishopMoves[j][1])):
                    break
                elif self.board[r + (i * bishopMoves[j][0])][c + (i * bishopMoves[j][1])] == "--":
                    moves.append(Move((r, c), (r + (i * bishopMoves[j][0]), c + (i * bishopMoves[j][1])), self.board))
                elif self.board[r + (i * bishopMoves[j][0])][c + (i * bishopMoves[j][1])][0] == color:
                    break
                elif self.board[r + (i * bishopMoves[j][0])][c + (i * bishopMoves[j][1])][0] != color:
                    moves.append(Move((r, c), (r + (i * bishopMoves[j][0]), c + (i * bishopMoves[j][1])), self.board))
                    break

    def getKnightMoves(self, r, c, color, moves):
        knightMoves = [(-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2)]
        for j in range(0, len(knightMoves)):
            if self.isOnBoard(r + knightMoves[j][0], c + knightMoves[j][1]):
                if self.board[r + knightMoves[j][0]][c + knightMoves[j][1]] == "--":
                    moves.append(Move((r, c), (r + knightMoves[j][0], c + knightMoves[j][1]), self.board))
                elif self.board[r + knightMoves[j][0]][c + knightMoves[j][1]][0] != color:
                    moves.append(Move((r, c), (r + knightMoves[j][0], c + knightMoves[j][1]), self.board))

    def getRookMoves(self, r, c, color, moves):
        rookMoves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for j in range(0, len(rookMoves)):
            for i in range(1, 8):
                if not self.isOnBoard(r + (i * rookMoves[j][0]), c + (i * rookMoves[j][1])):
                    break
                elif self.board[r + (i * rookMoves[j][0])][c + (i * rookMoves[j][1])] == "--":
                    moves.append(Move((r, c), (r + (i * rookMoves[j][0]), c + (i * rookMoves[j][1])), self.board))
                elif self.board[r + (i * rookMoves[j][0])][c + (i * rookMoves[j][1])][0] == color:
                    break
                elif self.board[r + (i * rookMoves[j][0])][c + (i * rookMoves[j][1])][0] != color:
                    moves.append(Move((r, c), (r + (i * rookMoves[j][0]), c + (i * rookMoves[j][1])), self.board))
                    break

    def getQueenMoves(self, r, c, color, moves):
        self.getBishopMoves(r, c, color, moves)
        self.getRookMoves(r, c, color, moves)

    def getKingMoves(self, r, c, color, moves):
        kingMoves = [(-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for j in range(0, len(kingMoves)):
            if self.isOnBoard(r + kingMoves[j][0], c + kingMoves[j][1]):
                if self.board[r + kingMoves[j][0]][c + kingMoves[j][1]] == "--":
                    moves.append(Move((r, c), (r + kingMoves[j][0], c + kingMoves[j][1]), self.board))
                elif self.board[r + kingMoves[j][0]][c + kingMoves[j][1]][0] != color:
                    moves.append(Move((r, c), (r + kingMoves[j][0], c + kingMoves[j][1]), self.board))

    def getKSCastlingMoves(self, r, c, color, moves):
        if self.hasCastlingRight[color + "ks"]:
            if (self.board[r][c+1] == "--") & (self.board[r][c+2] == "--") & (not self.squareUnderAttack(r, c+1, color)) & (not self.squareUnderAttack(r, c+2, color)):
                moves.append(Move((r, c), (r, c + 2), self.board, castling = True))
        return moves

    def getQSCastlingMoves(self, r, c, color, moves):
        if self.hasCastlingRight[color + "qs"]:
            if (self.board[r][c-1] == "--") & (self.board[r][c-2] == "--") & (self.board[r][c-3] == "--") & (not self.squareUnderAttack(r, c-1, color)) & (not self.squareUnderAttack(r, c-2, color)):
                moves.append(Move((r, c), (r, c - 2), self.board, castling = True))
        return moves

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

class Clock():

    def __init__(self, whiteBaseTime, whiteIncrement, blackBaseTime, blackIncrement):
        self.whiteBaseTime = whiteBaseTime * 60
        self.whiteIncrement = whiteIncrement
        self.blackBaseTime = blackBaseTime * 60
        self.blackIncrement = blackIncrement

    def increment(self, color):
        if color == "w":
            self.whiteBaseTime = self.whiteBaseTime + self.whiteIncrement
        elif color == "b":
            self.blackBaseTime = self.blackBaseTime + self.blackIncrement

    def updateClock(self, color):
        if color == "w":
            self.whiteBaseTime = self.whiteBaseTime - 1
        elif color == "b":
            self.blackBaseTime = self.blackBaseTime - 1