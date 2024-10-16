import copy

from Chess.src.Engine.Move import Move

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
        self.gameOver = False
        #initialize right to castle
        self.hasCastlingRight = {'wks': False, 'wqs': False, 'bks': False, 'bqs': False}
        self.castlingRightLost = {'wks': 0, 'wqs': 0, 'bks': 0, 'bqs': 0}
        #move number that color castled (positive = king side, negative = queen side)
        self.moveNumWhiteCastled = 0
        self.moveNumBlackCastled = 0
        if self.wKingLocation == (7, 4):
            if self.board[7][7] == "wR":
                self.hasCastlingRight['wks'] = True
                self.castlingRightLost['wks'] = -1
            if self.board[7][0] == "wR":
                self.hasCastlingRight['wqs'] = True
                self.castlingRightLost['wqs'] = -1
        if self.bKingLocation == (0, 4):
            if self.board[0][7] == "bR":
                self.hasCastlingRight['bks'] = True
                self.castlingRightLost['bks'] = -1
            if self.board[0][0] == "bR":
                self.hasCastlingRight['bqs'] = True
                self.castlingRightLost['bqs'] = -1
        self.noCaptureCount = 0
        #log of boards for purposes of determining draw by threefold repetition
        self.whiteBoards = [[copy.deepcopy(self.board), 1]]
        self.blackBoards = []
        self.legalMoves = []

    def resetGameState(self):
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
        self.gameOver = False
        #initialize right to castle
        self.hasCastlingRight = {'wks': False, 'wqs': False, 'bks': False, 'bqs': False}
        self.castlingRightLost = {'wks': 0, 'wqs': 0, 'bks': 0, 'bqs': 0}
        #move number that color castled (positive = king side, negative = queen side)
        self.moveNumWhiteCastled = 0
        self.moveNumBlackCastled = 0
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
        self.legalMoves = []

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
                if color == "w":
                    self.moveNumWhiteCastled = len(self.moveLog) + 1
                elif color == "b":
                    self.moveNumBlackCastled = len(self.moveLog) + 1
            elif move.endC == 6:
                self.board[move.endR][7] = "--"
                self.board[move.endR][move.endC - 1] = color + "R"
                if color == "w":
                    self.moveNumWhiteCastled = -1 * (len(self.moveLog) + 1)
                elif color == "b":
                    self.moveNumBlackCastled = -1 * (len(self.moveLog) + 1)
        #record capture count for 50 move rule
        if move.pieceCaptured == "--":
            self.noCaptureCount = self.noCaptureCount + 1
        else:
            self.noCaptureCount = 0
        self.moveLog.append(move)
        if self.noCaptureCount >= 50:
            pawnMoveCount = 0
            if len(self.moveLog) > 50:
                for index in range(1, 51):
                    if self.moveLog[-1 * index].pieceMoved[1] == "p":
                        pawnMoveCount = pawnMoveCount + 1
                if pawnMoveCount == 0:
                    self.fiftyMoveRuleDraw = True
        #record board for draw by repetition
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

    def undoMove(self):
        move = self.moveLog[-1]
        color = move.pieceMoved[0]
        self.deleteBoard() #remove last board from board log
        self.board[move.startR][move.startC] = move.pieceMoved
        self.board[move.endR][move.endC] = move.pieceCaptured
        if move.enPassant:
            if color == "w":
                self.board[move.endR + 1][move.endC] = "bp"
            elif color == "b":
                self.board[move.endR - 1][move.endC] = "wp"
        if move.castling:
            if abs(self.moveNumWhiteCastled) == len(self.moveLog):
                self.moveNumWhiteCastled = 0
            elif abs(self.moveNumBlackCastled) == len(self.moveLog):
                self.moveNumBlackCastled = 0
            if move.endC == 6:
                self.board[move.endR][move.endC - 1] = "--"
                self.board[move.startR][7] = color + "R"
            elif move.endC == 2:
                self.board[move.endR][move.endC + 1] = "--"
                self.board[move.startR][0] = color + "R"
        #undo changes to castling rights lost from last move
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
        if (move.pieceCaptured == "--") & (len(self.moveLog) > 0):
            self.noCaptureCount = self.noCaptureCount - 1
        elif len(self.moveLog) > 0:
            self.noCaptureCount = self.findNoCaptureCount()
        self.checkmate = False
        self.stalemate = False
        self.fiftyMoveRuleDraw = False
        self.drawByRepetition = False
        self.insufficientMaterial = False

    def stockfishMoveLog(self):
        stockfishMoveLog = []
        for move in self.moveLog:
            stockfishMoveLog.append(move.getRankFile(move.startR, move.startC) + move.getRankFile(move.endR, move.endC))
        return stockfishMoveLog


    def updateCastling(self):
        #remove correct castling rights on king and rook moves
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
        #remove king side castling rights
        if self.castlingRightLost[color + "ks"] < 0:
            self.hasCastlingRight[color + "ks"] = False
            self.castlingRightLost[color + "ks"] = len(self.moveLog)

    def updateQueenSideCastling(self, color):
        #remove queen side castling rights
        if self.castlingRightLost[color + "qs"] < 0:
            self.hasCastlingRight[color + "qs"] = False
            self.castlingRightLost[color + "qs"] = len(self.moveLog)

    def getLegalMoves(self): #considers checks from movement by taking all possibleMoves and identifying and removing moves that result in check
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

    def getPossibleMoves(self, color): #does not consider checks from movement, generates all moves by chess rules
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

    def squareUnderAttack(self, r, c, turn):
        oppMoves = self.getPossibleMoves(self.getOppColor(turn))
        #check if any opposing possible moves attacks given square
        for move in oppMoves:
            if (move.endR == r) & (move.endC == c):
                return True
        return False

    def findNoCaptureCount(self):
        #counts number of moves without a capture
        index = 1
        noCaptureCount = 0
        while (index < len(self.moveLog)) & (self.moveLog[-1 * index].pieceCaptured == "--"):
            noCaptureCount = noCaptureCount + 1
            index = index + 1
        return noCaptureCount

    def boardEquals(self, board):
        #check if given board is identical to current board
        for r in range(len(board)):
            for c in range(len(board[0])):
                if self.board[r][c] != board[r][c]:
                    return False
        return True

    def recordBoard(self):
        #add to correct board log
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
        #remove last recorded board
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
        #check for three occurences of same board
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
            if (boardPieceCount["wN"] == 0) & (boardPieceCount["wB"] == 0) & (boardPieceCount["bN"] == 0) & (boardPieceCount["bB"] == 0): #only kings on board
                return True
            elif ((boardPieceCount["wN"] == 0) & (boardPieceCount["bN"] == 0)) & (((boardPieceCount["wB"] == 1) & (boardPieceCount["bB"] == 0)) | ((boardPieceCount["wB"] == 0) & (boardPieceCount["bB"] == 1))): #only kings and one bishop
                return True
            elif ((boardPieceCount["wB"] == 0) & (boardPieceCount["bB"] == 0)) & (((boardPieceCount["wN"] == 1) & (boardPieceCount["bN"] == 0)) | ((boardPieceCount["wN"] == 0) & (boardPieceCount["bN"] == 1))): #only kings and one knight
                return True
            elif (boardPieceCount["wB"] == 1) & (boardPieceCount["bB"] == 1) & (len(bishopLocations) == 2): #only kings and two same square-color bishops
                firstBishopMoveModulo = (bishopLocations[0][0] + bishopLocations[0][1]) % 2
                secondBishopMoveModulo = (bishopLocations[1][0] + bishopLocations[1][1]) % 2
                if firstBishopMoveModulo == secondBishopMoveModulo:
                    return True
        return False

    def getPawnMoves(self, r, c, color, moves):
        if color == "w":
            if self.board[r-1][c] == "--": #move up one square
               moves.append(Move((r, c), (r-1, c), self.board))
               if r == 6:
                    if self.board[r-2][c] == "--": #move up two squares
                        moves.append(Move((r, c), (r-2, c), self.board))
            if ((c-1) >= 0):
                if (self.board[r-1][c-1][0] == "b"): #diagonal left capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if ((c+1) <= 7):
                if (self.board[r-1][c+1][0] == "b"): #diagonal right capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))
            if (r == 3) & (len(self.moveLog) > 0):
                if (self.moveLog[-1].startR == 1) & (self.moveLog[-1].endR == r):
                    if self.isOnBoard(r, c-1):
                        if (self.board[r][c-1] == "bp") & (self.moveLog[-1].startC == c-1) & (self.moveLog[-1].endC == c-1):
                            moves.append(Move((r, c), (r-1, c-1), self.board, enPassant = True)) #en passant left
                    if self.isOnBoard(r, c+1):
                        if (self.board[r][c+1] == "bp") & (self.moveLog[-1].startC == c+1) & (self.moveLog[-1].endC == c+1):
                            moves.append(Move((r, c), (r-1, c+1), self.board, enPassant = True)) #en passant right
        elif color == "b":
            if self.board[r+1][c] == "--": #move up one square
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1:
                    if self.board[r+2][c] == "--": #move up two squares
                        moves.append(Move((r, c), (r+2, c), self.board))
            if ((c-1) >= 0):
                if (self.board[r+1][c-1][0] == "w"): #diagonal left capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if ((c+1) <= 7):
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