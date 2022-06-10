import pygame as p
from playsound import playsound

from Chess.src.OtherStates.SpriteSheet import SpriteSheet
from Chess.src.Engine.Move import Move

class UserInterface():

    SIZE_MULTIPLIER = 8/3 #suggested (in order of largest to smallest window size): 2, 8/3, 4
    WINDOW_WIDTH = 2560 / SIZE_MULTIPLIER
    WINDOW_HEIGHT = 1800 / SIZE_MULTIPLIER
    WIDTH = HEIGHT = 1600 / SIZE_MULTIPLIER
    DIMENSION = 8
    SQ_SIZE = HEIGHT / DIMENSION
    FPS = 30
    IMAGES = [] #once populated, indices 0-23: pieces alternating between standard and leipzig, 24-27: cover, red in-check dot, green possible-move dot, possible-capture target
    PIECES = ["bR", "bN", "bB", "bQ", "bK", "bp", "wp", "wR", "wN", "wB", "wQ", "wK"]
    BOARD_COLORS = {"coffee": [p.Color("burlywood"), p.Color("salmon4")], "greyscale": [p.Color("gray90"), p.Color("gray60")]}
    
    def __init__(self):
        #initialize display
        p.init()
        self.screen = p.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.screen.fill(p.Color("white"))
        p.display.set_caption("Chess Engine")
        self.clock = p.time.Clock()
        self.loadImages()

        #menu screen
        self.oneMultiplayerStartButton = False
        self.twoMultiplayerStartButton = False
        self.singlePlayerStartButton = False
        self.settingsButton = False
        self.menuButtonWidth = self.WINDOW_WIDTH * (500 / 1280)
        self.menuButtonHeight = self.WINDOW_HEIGHT * (80 / 800)
        self.oneMultiplayerStartLoc = (((self.WINDOW_WIDTH - self.menuButtonWidth) / 2) - (self.WINDOW_WIDTH / 4.5), (self.WINDOW_HEIGHT - self.menuButtonHeight) / 1.5)
        self.twoMultiplayerStartLoc = (((self.WINDOW_WIDTH - self.menuButtonWidth) / 2) + (self.WINDOW_WIDTH / 4.5), (self.WINDOW_HEIGHT - self.menuButtonHeight) / 1.5)
        self.singlePlayerStartLoc = (((self.WINDOW_WIDTH - self.menuButtonWidth) / 2) - (self.WINDOW_WIDTH / 4.5), (self.WINDOW_HEIGHT - self.menuButtonHeight) / 1.2)
        self.settingsLoc = (((self.WINDOW_WIDTH - self.menuButtonWidth) / 2) + (self.WINDOW_WIDTH / 4.5), (self.WINDOW_HEIGHT - self.menuButtonHeight) / 1.2)

        #settings screen
        self.backButton = False
        self.settingsButtonWidth = self.WINDOW_WIDTH * (170 / 1280)
        self.settingsButtonHeight = self.WINDOW_HEIGHT * (60 / 800)
        self.backLoc = (self.WINDOW_WIDTH - self.settingsButtonWidth, self.WINDOW_HEIGHT - self.settingsButtonHeight)
        self.boardColorSchemeLoc = (0.2 * self.WINDOW_WIDTH, 0.28 * self.WINDOW_HEIGHT)
        self.moveHighlightingLoc = (0.2 * self.WINDOW_WIDTH, 0.47 * self.WINDOW_HEIGHT)
        self.autoQueenLoc = (0.2 * self.WINDOW_WIDTH, 0.66 * self.WINDOW_HEIGHT)
        self.pieceStyleLoc = ((0.8 * self.WINDOW_WIDTH) - (2 * self.settingsButtonWidth), 0.28 * self.WINDOW_HEIGHT)
        self.undoMoveLoc = ((0.8 * self.WINDOW_WIDTH) - (2 * self.settingsButtonWidth), 0.47 * self.WINDOW_HEIGHT)
        self.flipBoardLoc = ((0.8 * self.WINDOW_WIDTH) - (2 * self.settingsButtonWidth), 0.66 * self.WINDOW_HEIGHT)
        self.baseTimeLoc = (0.2 * self.WINDOW_WIDTH, 0.85 * self.WINDOW_HEIGHT)
        self.incrementTimeLoc = ((0.8 * self.WINDOW_WIDTH) - (2 * self.settingsButtonWidth), 0.85 * self.WINDOW_HEIGHT)

    def loadImages(self):
        #load spritesheet of standard pieces
        stanPieces = SpriteSheet(p.image.load("../../assets/images/standardpieces.png"), 2, 6)
        #get part of spritesheet that is that specific standard piece
        standardwK = stanPieces.getSubImageByIndex(0, 0)
        standardwQ = stanPieces.getSubImageByIndex(0, 1)
        standardwB = stanPieces.getSubImageByIndex(0, 2)
        standardwN = stanPieces.getSubImageByIndex(0, 3)
        standardwR = stanPieces.getSubImageByIndex(0, 4)
        standardwp = stanPieces.getSubImageByIndex(0, 5)
        standardbK = stanPieces.getSubImageByIndex(1, 0)
        standardbQ = stanPieces.getSubImageByIndex(1, 1)
        standardbB = stanPieces.getSubImageByIndex(1, 2)
        standardbN = stanPieces.getSubImageByIndex(1, 3)
        standardbR = stanPieces.getSubImageByIndex(1, 4)
        standardbp = stanPieces.getSubImageByIndex(1, 5)
        for piece in self.PIECES:
            #scale subimages and add to IMAGES array
            if piece[0] == "b":
                if piece[1] == "K":
                    self.IMAGES.append(p.transform.scale(standardbK, (self.SQ_SIZE, self.SQ_SIZE)))
                elif piece[1] == "Q":
                    self.IMAGES.append(p.transform.scale(standardbQ, (self.SQ_SIZE, self.SQ_SIZE)))
                elif piece[1] == "R":
                    self.IMAGES.append(p.transform.scale(standardbR, (self.SQ_SIZE, self.SQ_SIZE)))
                elif piece[1] == "B":
                    self.IMAGES.append(p.transform.scale(standardbB, (self.SQ_SIZE, self.SQ_SIZE)))
                elif piece[1] == "N":
                    self.IMAGES.append(p.transform.scale(standardbN, (self.SQ_SIZE, self.SQ_SIZE)))
                elif piece[1] == "p":
                    self.IMAGES.append(p.transform.scale(standardbp, (self.SQ_SIZE, self.SQ_SIZE)))
            elif piece[0] == "w":
                if piece[1] == "K":
                    self.IMAGES.append(p.transform.scale(standardwK, (self.SQ_SIZE, self.SQ_SIZE)))
                elif piece[1] == "Q":
                    self.IMAGES.append(p.transform.scale(standardwQ, (self.SQ_SIZE, self.SQ_SIZE)))
                elif piece[1] == "R":
                    self.IMAGES.append(p.transform.scale(standardwR, (self.SQ_SIZE, self.SQ_SIZE)))
                elif piece[1] == "B":
                    self.IMAGES.append(p.transform.scale(standardwB, (self.SQ_SIZE, self.SQ_SIZE)))
                elif piece[1] == "N":
                    self.IMAGES.append(p.transform.scale(standardwN, (self.SQ_SIZE, self.SQ_SIZE)))
                elif piece[1] == "p":
                    self.IMAGES.append(p.transform.scale(standardwp, (self.SQ_SIZE, self.SQ_SIZE)))
            #for all pieces in PIECES array, load and add corresponding leipzig piece to IMAGES array
            self.IMAGES.append(p.transform.scale(p.image.load("../../assets/images/leipzigPieces/leipzig" + piece +".png"), (self.SQ_SIZE, self.SQ_SIZE))) #load leipzig pieces

        #load and add other non-piece images to IMAGES array
        self.IMAGES.append(p.transform.scale(p.image.load("../../assets/images/cover.png"), (1563 / (2560 / self.WINDOW_WIDTH), 1042 / (1800 / self.WINDOW_HEIGHT))))
        self.IMAGES.append(p.transform.scale(p.image.load("../../assets/images/reddot.png"), (self.SQ_SIZE, self.SQ_SIZE)))
        self.IMAGES.append(p.transform.scale(p.image.load("../../assets/images/dot.png"), (self.SQ_SIZE, self.SQ_SIZE)))
        self.IMAGES.append(p.transform.scale(p.image.load("../../assets/images/target.png"), (self.SQ_SIZE, self.SQ_SIZE)))

    def printGameInstructions(self):
        print(" ")
        print("Hello and welcome to Rohil's chess engine!")
        print("Adjust your settings or start a game. Note that some settings are pre-set for the two-machine multiplayer game mode.")
        print("Here are some keyboard controls you should know:")
        print("If you have auto queen disabled, when promoting a pawn, use the 'q', 'r', 'n', and 'b' keys to make your promotion choice.")
        print("If you have undo move enabled, use the 'backspace' key to undo a move. This setting is not available in the two-machine multiplayer game mode.")
        print("To reset the game at any time in the one-machine multiplayer or single player game modes, press the 'x' key.")
        print("Good luck player and feel free to leave feedback!")
        print(" ")


    def drawMenuState(self):
        self.screen.fill(p.Color("white"))
        TEXT_FONT = p.font.SysFont('arial', int(self.WINDOW_WIDTH * (28 / 1280)), False, False)
        TEXT_COLOR = p.Color("white")
        buttonColor = p.Color("black")

        #draw One Multiplayer Start button
        p.draw.rect(self.screen, buttonColor, p.Rect(self.oneMultiplayerStartLoc[0], self.oneMultiplayerStartLoc[1], self.menuButtonWidth, self.menuButtonHeight))
        startText = TEXT_FONT.render("Start Multiplayer - One Machine", 0, TEXT_COLOR)
        self.screen.blit(startText, (self.oneMultiplayerStartLoc[0] + ((self.menuButtonWidth - startText.get_width()) / 2), self.oneMultiplayerStartLoc[1] + ((self.menuButtonHeight - startText.get_height()) / 2)))

        #draw Two Multiplayer Start button
        p.draw.rect(self.screen, buttonColor, p.Rect(self.twoMultiplayerStartLoc[0], self.twoMultiplayerStartLoc[1], self.menuButtonWidth, self.menuButtonHeight))
        startText = TEXT_FONT.render("Start Multiplayer - Two Machines", 0, TEXT_COLOR)
        self.screen.blit(startText, (self.twoMultiplayerStartLoc[0] + ((self.menuButtonWidth - startText.get_width()) / 2), self.twoMultiplayerStartLoc[1] + ((self.menuButtonHeight - startText.get_height()) / 2)))

        #draw Single Player Start button
        p.draw.rect(self.screen, buttonColor, p.Rect(self.singlePlayerStartLoc[0], self.singlePlayerStartLoc[1], self.menuButtonWidth, self.menuButtonHeight))
        startText = TEXT_FONT.render("Start Single Player", 0, TEXT_COLOR)
        self.screen.blit(startText, (self.singlePlayerStartLoc[0] + ((self.menuButtonWidth - startText.get_width()) / 2), self.singlePlayerStartLoc[1] + ((self.menuButtonHeight - startText.get_height()) / 2)))

        #draw Settings button
        p.draw.rect(self.screen, buttonColor, p.Rect(self.settingsLoc[0], self.settingsLoc[1], self.menuButtonWidth, self.menuButtonHeight))
        settingsText = TEXT_FONT.render("Settings", 0, TEXT_COLOR)
        self.screen.blit(settingsText, (self.settingsLoc[0] + ((self.menuButtonWidth - settingsText.get_width()) / 2), self.settingsLoc[1] + ((self.menuButtonHeight - settingsText.get_height()) / 2)))

        self.screen.blit(self.IMAGES[-4], p.Rect((self.WINDOW_WIDTH - self.IMAGES[-4].get_width()) / 2, (self.twoMultiplayerStartLoc[1] - self.IMAGES[-4].get_height()) / 2, self.IMAGES[-4].get_width(), self.IMAGES[-4].get_height()))

    def checkOneMultiplayerStartButtonPressed(self):
        if (self.oneMultiplayerStartLoc[0] < p.mouse.get_pos()[0] < (self.oneMultiplayerStartLoc[0] + self.menuButtonWidth)) & (self.oneMultiplayerStartLoc[1] < p.mouse.get_pos()[1] < (self.oneMultiplayerStartLoc[1] + self.menuButtonHeight)):
            self.oneMultiplayerStartButton = True

    def checkTwoMultiplayerStartButtonPressed(self):
        if (self.twoMultiplayerStartLoc[0] < p.mouse.get_pos()[0] < (self.twoMultiplayerStartLoc[0] + self.menuButtonWidth)) & (self.twoMultiplayerStartLoc[1] < p.mouse.get_pos()[1] < (self.twoMultiplayerStartLoc[1] + self.menuButtonHeight)):
            self.twoMultiplayerStartButton = True

    def checkSinglePlayerStartButtonPressed(self):
        if (self.singlePlayerStartLoc[0] < p.mouse.get_pos()[0] < (self.singlePlayerStartLoc[0] + self.menuButtonWidth)) & (self.singlePlayerStartLoc[1] < p.mouse.get_pos()[1] < (self.singlePlayerStartLoc[1] + self.menuButtonHeight)):
            self.singlePlayerStartButton = True

    def checkSettingsButtonPressed(self):
        if (self.settingsLoc[0] < p.mouse.get_pos()[0] < (self.settingsLoc[0] + self.menuButtonWidth)) & (self.settingsLoc[1] < p.mouse.get_pos()[1] < (self.settingsLoc[1] + self.menuButtonHeight)):
            self.settingsButton = True


    def drawEndOfGame(self, state, color = "None"):
        TEXT_COLOR = p.Color("white")
        TEXT_FONT = p.font.SysFont('arial', int(self.WINDOW_WIDTH * (30 / 1280)), True, False)

        rectSize = (self.WIDTH / 2, self.HEIGHT / 10)
        rectPos = ((self.WIDTH - rectSize[0]) / 2, (self.HEIGHT - rectSize[1]) / 2)

        if state == "checkmate":
            if color == "w":
                winColor = "White"
            else:
                winColor = "Black"
            text = TEXT_FONT.render(winColor + " wins by checkmate.", 0, TEXT_COLOR)
        elif state == "stalemate":
            text = TEXT_FONT.render("Draw by stalemate.", 0, TEXT_COLOR)
        elif state == "insufficientMaterial":
            text = TEXT_FONT.render("Draw by insufficient material.", 0, TEXT_COLOR)
        elif state == "repetition":
            text = TEXT_FONT.render("Draw by repetition.", 0, TEXT_COLOR)
        elif state == "fiftyMove":
            text = TEXT_FONT.render("Draw by fifty move rule.", 0, TEXT_COLOR)
        elif state == "whiteTimeout":
            text = TEXT_FONT.render("White timeout. Black wins.", 0, TEXT_COLOR)
        elif state == "blackTimeout":
            text = TEXT_FONT.render("Black timeout. White wins.", 0, TEXT_COLOR)

        rectSize = (text.get_width() * 1.5, text.get_height() * 2.5)
        rectPos = ((self.WIDTH - rectSize[0]) / 2, (self.HEIGHT - rectSize[1]) / 2)
        rect = p.Surface(rectSize)
        rect.set_alpha(200) #set opacity
        rect.fill((0, 0, 0))
        self.screen.blit(rect, rectPos)

        self.screen.blit(text, (rectPos[0] + ((rectSize[0] - text.get_width()) / 2), rectPos[1] + ((rectSize[1] - text.get_height()) / 2)))

    def drawGameState(self, gs, ss, sqSelected, legalMoves, gameClock, whiteClockOn, mode, premoveSqSelected = None, premove = None):
        self.screen.fill(p.Color("white"))
        self.drawBoard(gs, ss, mode)
        self.drawSelected(gs, ss, sqSelected, legalMoves, mode, ss.highlightValidMoves)
        if (type(premoveSqSelected) == tuple):
            self.drawPremove(gs, ss, premoveSqSelected, premove, mode)
        self.drawPieces(gs, ss, mode)
        self.renderMoveHistory(gs)
        self.displayClock(gameClock, whiteClockOn)

    def drawBoard(self, gs, ss, mode):
        colors = self.BOARD_COLORS[ss.boardColorScheme]
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                p.draw.rect(self.screen, colors[(self.adjustForFlipBoard(r, gs.whiteToMove, ss.flipBoard, mode) + self.adjustForFlipBoard(c, gs.whiteToMove, ss.flipBoard, mode)) % 2], p.Rect(self.adjustForFlipBoard(c, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.adjustForFlipBoard(r, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
        if gs.inCheck("w"):
            self.screen.blit(self.IMAGES[-3], p.Rect(self.adjustForFlipBoard(gs.wKingLocation[1], gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.adjustForFlipBoard(gs.wKingLocation[0], gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
        if gs.inCheck("b"):
            self.screen.blit(self.IMAGES[-3], p.Rect(self.adjustForFlipBoard(gs.bKingLocation[1], gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.adjustForFlipBoard(gs.bKingLocation[0], gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def drawPieces(self, gs, ss, mode):
        if ss.pieceStyle == "standard":
            constant = 0
        elif ss.pieceStyle == "leipzig":
            constant = 1
        for r in range(self.DIMENSION):
            for c in range(self.DIMENSION):
                piece = gs.board[r][c]
                if piece != "--":
                    self.screen.blit(self.IMAGES[(2 * self.PIECES.index(piece)) + constant], p.Rect(self.adjustForFlipBoard(c, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.adjustForFlipBoard(r, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def drawSelected(self, gs, ss, sqSelected, legalMoves, mode, highlightValidMoves):
        if (len(sqSelected) > 0):
            if gs.board[int(sqSelected[0])][int(sqSelected[1])][0] == gs.getTurnColor():
                p.draw.rect(self.screen, p.Color("palegreen4"), p.Rect(self.adjustForFlipBoard(int(sqSelected[1]), gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.adjustForFlipBoard(int(sqSelected[0]), gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
                if highlightValidMoves:
                    for move in legalMoves:
                        if (move.startR == int(sqSelected[0])) & (move.startC == int(sqSelected[1])):
                            if move.pieceCaptured == "--":
                                self.screen.blit(self.IMAGES[-2], p.Rect(self.adjustForFlipBoard(move.endC, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.adjustForFlipBoard(move.endR, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
                            elif (gs.whiteToMove & (move.pieceCaptured[0] == "b")) | ((not gs.whiteToMove) & (move.pieceCaptured[0] == "w")):
                                self.screen.blit(self.IMAGES[-1], p.Rect(self.adjustForFlipBoard(move.endC, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.adjustForFlipBoard(move.endR, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

    def drawPremove(self, gs, ss, premoveSqSelected, premove, mode):
        SELECT_COLOR = p.Color("cadetblue3")
        PREMOVE_COLOR = p.Color("cadetblue4")
        if isinstance(premove, Move):
            p.draw.rect(self.screen, PREMOVE_COLOR, p.Rect(self.adjustForFlipBoard(premove.startC, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.adjustForFlipBoard(premove.startR, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
            p.draw.rect(self.screen, PREMOVE_COLOR, p.Rect(self.adjustForFlipBoard(premove.endC, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.adjustForFlipBoard(premove.endR, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
        elif (len(premoveSqSelected) > 0):
            if gs.board[int(premoveSqSelected[0])][int(premoveSqSelected[1])][0] == gs.getOppColor(gs.getTurnColor()):
                p.draw.rect(self.screen, SELECT_COLOR, p.Rect(self.adjustForFlipBoard(int(premoveSqSelected[1]), gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.adjustForFlipBoard(int(premoveSqSelected[0]), gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))


    def animateMove(self, gs, ss, mode):
        if len(gs.moveLog) > 0:
            move = gs.moveLog[-1]
            if move.pieceCaptured == "--":
                playsound("../../assets/sounds/move_sound.mp3")
            else:
                playsound("../../assets/sounds/capture_sound.mp3")
            frameCount = int(((ss.clockLength * 5) + (ss.clockIncrement * 10)) / 30) #num of frames over which animation occurs
            if frameCount > 0:
                animationFPS = 60
                delta_r = move.endR - move.startR
                delta_c = move.endC - move.startC
                if ss.pieceStyle == "standard":
                    constant = 0
                elif ss.pieceStyle == "leipzig":
                    constant = 1
                for frame in range(frameCount + 1):
                    r, c = (move.startR + ((frame / frameCount) * delta_r), move.startC + ((frame / frameCount) * delta_c))
                    #draw board and pieces
                    self.drawBoard(gs, ss, mode)
                    self.drawPieces(gs, ss, mode)
                    #erase start and end squares
                    startSquare = p.Rect(self.adjustForFlipBoard(move.startC, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.adjustForFlipBoard(move.startR, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE)
                    p.draw.rect(self.screen, self.BOARD_COLORS[ss.boardColorScheme][(self.adjustForFlipBoard(move.startR, gs.whiteToMove, ss.flipBoard, mode) + self.adjustForFlipBoard(move.startC, gs.whiteToMove, ss.flipBoard, mode)) % 2], startSquare)
                    endSquare = p.Rect(self.adjustForFlipBoard(move.endC, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.adjustForFlipBoard(move.endR, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE)
                    p.draw.rect(self.screen, self.BOARD_COLORS[ss.boardColorScheme][(self.adjustForFlipBoard(move.endR, gs.whiteToMove, ss.flipBoard, mode) + self.adjustForFlipBoard(move.endC, gs.whiteToMove, ss.flipBoard, mode)) % 2], endSquare)
                    #if piece will be captured, redraw captured piece
                    if move.pieceCaptured != "--":
                        self.screen.blit(self.IMAGES[(2 * self.PIECES.index(move.pieceCaptured)) + constant], p.Rect(self.adjustForFlipBoard(move.endC, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.adjustForFlipBoard(move.endR, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
                    #draw moved piece at animated coordinates
                    self.screen.blit(self.IMAGES[(2 * self.PIECES.index(move.pieceMoved)) + constant], p.Rect(self.adjustForFlipBoard(c, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.adjustForFlipBoard(r, gs.whiteToMove, ss.flipBoard, mode) * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))

                    self.flipDisplay()
                    self.tickClock(FPS = animationFPS)

    def adjustForFlipBoard(self, num, whiteTurn, flipBoard, mode):
        if mode == "oneMultiplayer":
            if flipBoard & (not whiteTurn):
                return abs(7 - num)
            else:
                return num
        elif (mode == "twoMultiplayer") | (mode == "singlePlayer"):
            if flipBoard:
                return abs(7 - num)
            else:
                return num

    def renderMoveHistory(self, gs):
        if len(gs.moveLog) > 80:
            FONT_SIZE = int(self.WINDOW_WIDTH * (24 / 1280))
        else:
            FONT_SIZE = int(self.WINDOW_WIDTH * (28 / 1280))
        FONT_SIZE = int(self.WINDOW_WIDTH * (28 / 1280))
        TEXT_FONT = p.font.SysFont('arial', FONT_SIZE, False, False)
        TEXTBOX_X = self.WIDTH
        TEXTBOX_Y = 0
        TEXTBOX_WIDTH = int(self.WINDOW_WIDTH - self.WIDTH)
        TEXTBOX_HEIGHT = self.HEIGHT
        TEXT_COLOR = p.Color("black")
        TEXTBOX_COLOR = p.Color("light gray")
        moveLogText = []
        space = TEXT_FONT.size(" ")[0]
        p.draw.rect(self.screen, TEXTBOX_COLOR, p.Rect(TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT))
        for item in gs.moveLog:
            moveLogText.append(item.notation + " ")
        if len(moveLogText) > 0:
            moveLogText[-1] = (moveLogText[-1])[:-1]
        MAX_WIDTH = 0.9 * TEXTBOX_WIDTH
        LOG_X = TEXTBOX_X + ((TEXTBOX_WIDTH - MAX_WIDTH) / 2)
        MAX_HEIGHT = 0.94 * TEXTBOX_HEIGHT
        LOG_Y = TEXTBOX_Y + ((TEXTBOX_HEIGHT - MAX_HEIGHT) / 2)
        x = LOG_X
        y = LOG_Y
        for item in moveLogText:
            log_screen = TEXT_FONT.render(item, 0, TEXT_COLOR)
            item_width, item_height = log_screen.get_size()
            if x + item_width >= MAX_WIDTH + LOG_X: #create new row
                x = LOG_X
                y += 1.2 * item_height
            self.screen.blit(log_screen, (x, y))
            x += item_width + space #can remove space - stylistic choice


    def displayClock(self, gameClock, whiteClockOn):
        TEXT_FONT = p.font.SysFont('arial', int(self.WINDOW_WIDTH * (80 / 1280)), False, False)
        LABEL_FONT = p.font.SysFont('arial', int(self.WINDOW_WIDTH * (26 / 1280)), False, False)
        WHITE_CLOCK_X = 0
        BLACK_CLOCK_X = self.WINDOW_WIDTH / 2
        CLOCK_Y = self.HEIGHT
        CLOCK_WIDTH = self.WINDOW_WIDTH / 2
        CLOCK_HEIGHT = self.WINDOW_HEIGHT - self.HEIGHT
        TEXT_COLOR = p.Color("black")
        ON_COLOR = p.Color("olivedrab4")
        OFF_COLOR = p.Color("gray60")
        LOW_TIME_ON_COLOR = p.Color("firebrick2")
        LOW_TIME_OFF_COLOR = p.Color("tomato2")

        if whiteClockOn:
            if gameClock.whiteBaseTime < gameClock.lowTimeThreshold:
                whiteColor = LOW_TIME_ON_COLOR
            else:
                whiteColor = ON_COLOR
            if gameClock.blackBaseTime < gameClock.lowTimeThreshold:
                blackColor = LOW_TIME_OFF_COLOR
            else:
                blackColor = OFF_COLOR
        else:
            if gameClock.whiteBaseTime < gameClock.lowTimeThreshold:
                whiteColor = LOW_TIME_OFF_COLOR
            else:
                whiteColor = OFF_COLOR
            if gameClock.blackBaseTime < gameClock.lowTimeThreshold:
                blackColor = LOW_TIME_ON_COLOR
            else:
                blackColor = ON_COLOR

        #white clock
        p.draw.rect(self.screen, whiteColor, p.Rect(WHITE_CLOCK_X, CLOCK_Y, CLOCK_WIDTH, CLOCK_HEIGHT))
        white_hours = int(gameClock.whiteBaseTime / (3600 * 1000))
        white_minutes = int((gameClock.whiteBaseTime - (white_hours * 3600 * 1000)) / (60 * 1000))
        white_seconds = int((gameClock.whiteBaseTime - (white_minutes * 60 * 1000)) / (1000))
        whiteTimeText = TEXT_FONT.render(str(white_hours) + ":" + str(white_minutes).zfill(2) + ":" + str(white_seconds).zfill(2), 0, TEXT_COLOR)
        self.screen.blit(whiteTimeText, (WHITE_CLOCK_X + ((CLOCK_WIDTH - whiteTimeText.get_width()) / 2), CLOCK_Y + ((CLOCK_HEIGHT - whiteTimeText.get_height()) / 2)))

        #black clock
        p.draw.rect(self.screen, blackColor, p.Rect(BLACK_CLOCK_X, CLOCK_Y, CLOCK_WIDTH, CLOCK_HEIGHT))
        black_hours = int(gameClock.blackBaseTime / (3600 * 1000))
        black_minutes = int((gameClock.blackBaseTime - (black_hours * 3600 * 1000)) / (60 * 1000))
        black_seconds = int((gameClock.blackBaseTime - (black_minutes * 60 * 1000)) / (1000))
        blackTimeText = TEXT_FONT.render(str(black_hours) + ":" + str(black_minutes).zfill(2) + ":" + str(black_seconds).zfill(2), 0, TEXT_COLOR)
        self.screen.blit(blackTimeText, (BLACK_CLOCK_X + ((CLOCK_WIDTH - blackTimeText.get_width()) / 2), CLOCK_Y + ((CLOCK_HEIGHT - blackTimeText.get_height()) / 2)))

        #draw white rotated label
        whiteTimeLabel = LABEL_FONT.render("WHITE", 0, TEXT_COLOR)
        whiteTimeLabel = p.transform.rotate(whiteTimeLabel, 90)
        self.screen.blit(whiteTimeLabel, (WHITE_CLOCK_X + (0.1 * whiteTimeLabel.get_width()), CLOCK_Y + ((CLOCK_HEIGHT - whiteTimeLabel.get_height()) / 2)))

        #draw black rotated label
        blackTimeLabel = LABEL_FONT.render("BLACK", 0, TEXT_COLOR)
        blackTimeLabel = p.transform.rotate(blackTimeLabel, 90)
        self.screen.blit(blackTimeLabel, (BLACK_CLOCK_X + (0.1 * blackTimeLabel.get_width()), CLOCK_Y + ((CLOCK_HEIGHT - blackTimeLabel.get_height()) / 2)))


    def drawSettingsState(self, ss):
        self.screen.fill(p.Color("white"))

        TITLE_TEXT_FONT = p.font.SysFont('arial', int(self.WINDOW_WIDTH * (80 / 1280)), True, False)
        TITLE_TEXT_COLOR = p.Color("black")
        LABEL_FONT = p.font.SysFont('arial', int(self.WINDOW_WIDTH * (40 / 1280)), False, False)
        LABEL_COLOR = p.Color("black")
        TEXT_FONT = p.font.SysFont('arial', int(self.WINDOW_WIDTH * (28 / 1280)), False, False)
        TEXT_COLOR = p.Color("white")

        titleText = TITLE_TEXT_FONT.render("SETTINGS", 0, TITLE_TEXT_COLOR)
        self.screen.blit(titleText, ((self.WINDOW_WIDTH - titleText.get_width()) / 2, self.WINDOW_HEIGHT / 20))

        #draw Back button
        p.draw.rect(self.screen, p.Color("firebrick1"), p.Rect(self.backLoc[0], self.backLoc[1], self.settingsButtonWidth, self.settingsButtonHeight))
        backText = TEXT_FONT.render("Back", 0, TEXT_COLOR)
        self.screen.blit(backText, (self.backLoc[0] + ((self.settingsButtonWidth - backText.get_width()) / 2), self.backLoc[1] + ((self.settingsButtonHeight - backText.get_height()) / 2)))

        #draw Board Color Scheme Settings buttons
        boardColorSchemeLabel = LABEL_FONT.render("Board Color Scheme", 0, LABEL_COLOR)
        p.draw.rect(self.screen, self.getSettingButtonColor(ss, "boardColorScheme", "coffee"), p.Rect(self.boardColorSchemeLoc[0], self.boardColorSchemeLoc[1], self.settingsButtonWidth, self.settingsButtonHeight))
        boardColorCoffeeText = TEXT_FONT.render("Coffee", 0, TEXT_COLOR)
        p.draw.rect(self.screen, self.getSettingButtonColor(ss, "boardColorScheme", "greyscale"), p.Rect(self.boardColorSchemeLoc[0] + self.settingsButtonWidth, self.boardColorSchemeLoc[1], self.settingsButtonWidth, self.settingsButtonHeight))
        boardColorGreyscaleText = TEXT_FONT.render("Greyscale", 0, TEXT_COLOR)
        self.screen.blit(boardColorSchemeLabel, (self.boardColorSchemeLoc[0] + (((2 * self.settingsButtonWidth) - boardColorSchemeLabel.get_width()) / 2), self.boardColorSchemeLoc[1] - (1.5 * boardColorSchemeLabel.get_height())))
        self.screen.blit(boardColorCoffeeText, (self.boardColorSchemeLoc[0] + ((self.settingsButtonWidth - boardColorCoffeeText.get_width()) / 2), self.boardColorSchemeLoc[1] + ((self.settingsButtonHeight - boardColorCoffeeText.get_height()) / 2)))
        self.screen.blit(boardColorGreyscaleText, (self.boardColorSchemeLoc[0] + self.settingsButtonWidth + ((self.settingsButtonWidth - boardColorGreyscaleText.get_width()) / 2), self.boardColorSchemeLoc[1] + ((self.settingsButtonHeight - boardColorGreyscaleText.get_height()) / 2)))

        #draw Move Highlighting Settings buttons
        moveHighlightingLabel = LABEL_FONT.render("Move Highlighting", 0, LABEL_COLOR)
        p.draw.rect(self.screen, self.getSettingButtonColor(ss, "moveHighlighting", "on"), p.Rect(self.moveHighlightingLoc[0], self.moveHighlightingLoc[1], self.settingsButtonWidth, self.settingsButtonHeight))
        moveHighlightingOnText = TEXT_FONT.render("Enabled", 0, TEXT_COLOR)
        p.draw.rect(self.screen, self.getSettingButtonColor(ss, "moveHighlighting", "off"), p.Rect(self.moveHighlightingLoc[0] + self.settingsButtonWidth, self.moveHighlightingLoc[1], self.settingsButtonWidth, self.settingsButtonHeight))
        moveHighlightingOffText = TEXT_FONT.render("Disabled", 0, TEXT_COLOR)
        self.screen.blit(moveHighlightingLabel, (self.moveHighlightingLoc[0] + (((2 * self.settingsButtonWidth) - moveHighlightingLabel.get_width()) / 2), self.moveHighlightingLoc[1] - (1.5 * moveHighlightingLabel.get_height())))
        self.screen.blit(moveHighlightingOnText, (self.moveHighlightingLoc[0] + ((self.settingsButtonWidth - moveHighlightingOnText.get_width()) / 2), self.moveHighlightingLoc[1] + ((self.settingsButtonHeight - moveHighlightingOnText.get_height()) / 2)))
        self.screen.blit(moveHighlightingOffText, (self.moveHighlightingLoc[0] + self.settingsButtonWidth + ((self.settingsButtonWidth - moveHighlightingOffText.get_width()) / 2), self.moveHighlightingLoc[1] + ((self.settingsButtonHeight - moveHighlightingOffText.get_height()) / 2)))

        #draw Auto Queen Settings buttons
        autoQueenLabel = LABEL_FONT.render("Auto Queen", 0, LABEL_COLOR)
        p.draw.rect(self.screen, self.getSettingButtonColor(ss, "autoQueen", "on"), p.Rect(self.autoQueenLoc[0], self.autoQueenLoc[1], self.settingsButtonWidth, self.settingsButtonHeight))
        autoQueenOnText = TEXT_FONT.render("Enabled", 0, TEXT_COLOR)
        p.draw.rect(self.screen, self.getSettingButtonColor(ss, "autoQueen", "off"), p.Rect(self.autoQueenLoc[0] + self.settingsButtonWidth, self.autoQueenLoc[1], self.settingsButtonWidth, self.settingsButtonHeight))
        autoQueenOffText = TEXT_FONT.render("Disabled", 0, TEXT_COLOR)
        self.screen.blit(autoQueenLabel, (self.autoQueenLoc[0] + (((2 * self.settingsButtonWidth) - autoQueenLabel.get_width()) / 2), self.autoQueenLoc[1] - (1.5 * autoQueenLabel.get_height())))
        self.screen.blit(autoQueenOnText, (self.autoQueenLoc[0] + ((self.settingsButtonWidth - autoQueenOnText.get_width()) / 2), self.autoQueenLoc[1] + ((self.settingsButtonHeight - autoQueenOnText.get_height()) / 2)))
        self.screen.blit(autoQueenOffText, (self.autoQueenLoc[0] + self.settingsButtonWidth + ((self.settingsButtonWidth - autoQueenOffText.get_width()) / 2), self.autoQueenLoc[1] + ((self.settingsButtonHeight - autoQueenOffText.get_height()) / 2)))

        #draw Piece Style Settings buttons
        pieceStyleLabel = LABEL_FONT.render("Piece Style", 0, LABEL_COLOR)
        p.draw.rect(self.screen, self.getSettingButtonColor(ss, "pieceStyle", "standard"), p.Rect(self.pieceStyleLoc[0], self.pieceStyleLoc[1], self.settingsButtonWidth, self.settingsButtonHeight))
        standardPieceStyleText = TEXT_FONT.render("Standard", 0, TEXT_COLOR)
        p.draw.rect(self.screen, self.getSettingButtonColor(ss, "pieceStyle", "leipzig"), p.Rect(self.pieceStyleLoc[0] + self.settingsButtonWidth, self.pieceStyleLoc[1], self.settingsButtonWidth, self.settingsButtonHeight))
        leipzigPieceStyleText = TEXT_FONT.render("Leipzig", 0, TEXT_COLOR)
        self.screen.blit(pieceStyleLabel, (self.pieceStyleLoc[0] + (((2 * self.settingsButtonWidth) - pieceStyleLabel.get_width()) / 2), self.pieceStyleLoc[1] - (1.5 * pieceStyleLabel.get_height())))
        self.screen.blit(standardPieceStyleText, (self.pieceStyleLoc[0] + ((self.settingsButtonWidth - standardPieceStyleText.get_width()) / 2), self.pieceStyleLoc[1] + ((self.settingsButtonHeight - standardPieceStyleText.get_height()) / 2)))
        self.screen.blit(leipzigPieceStyleText, (self.pieceStyleLoc[0] + self.settingsButtonWidth + ((self.settingsButtonWidth - leipzigPieceStyleText.get_width()) / 2), self.pieceStyleLoc[1] + ((self.settingsButtonHeight - leipzigPieceStyleText.get_height()) / 2)))

        #draw Undo Move Enabling Settings buttons
        undoMoveLabel = LABEL_FONT.render("Undo Move", 0, LABEL_COLOR)
        p.draw.rect(self.screen, self.getSettingButtonColor(ss, "undoMove", "on"), p.Rect(self.undoMoveLoc[0], self.undoMoveLoc[1], self.settingsButtonWidth, self.settingsButtonHeight))
        undoMoveOnText = TEXT_FONT.render("Enabled", 0, TEXT_COLOR)
        p.draw.rect(self.screen, self.getSettingButtonColor(ss, "undoMove", "off"), p.Rect(self.undoMoveLoc[0] + self.settingsButtonWidth, self.undoMoveLoc[1], self.settingsButtonWidth, self.settingsButtonHeight))
        undoMoveOffText = TEXT_FONT.render("Disabled", 0, TEXT_COLOR)
        self.screen.blit(undoMoveLabel, (self.undoMoveLoc[0] + (((2 * self.settingsButtonWidth) - undoMoveLabel.get_width()) / 2), self.undoMoveLoc[1] - (1.5 * undoMoveLabel.get_height())))
        self.screen.blit(undoMoveOnText, (self.undoMoveLoc[0] + ((self.settingsButtonWidth - undoMoveOnText.get_width()) / 2), self.undoMoveLoc[1] + ((self.settingsButtonHeight - undoMoveOnText.get_height()) / 2)))
        self.screen.blit(undoMoveOffText, (self.undoMoveLoc[0] + self.settingsButtonWidth + ((self.settingsButtonWidth - undoMoveOffText.get_width()) / 2), self.undoMoveLoc[1] + ((self.settingsButtonHeight - undoMoveOffText.get_height()) / 2)))

        #draw Flip Board Enabling Settings buttons
        flipBoardLabel = LABEL_FONT.render("Flip Board", 0, LABEL_COLOR)
        p.draw.rect(self.screen, self.getSettingButtonColor(ss, "flipBoard", "on"), p.Rect(self.flipBoardLoc[0], self.flipBoardLoc[1], self.settingsButtonWidth, self.settingsButtonHeight))
        flipBoardOnText = TEXT_FONT.render("Enabled", 0, TEXT_COLOR)
        p.draw.rect(self.screen, self.getSettingButtonColor(ss, "flipBoard", "off"), p.Rect(self.flipBoardLoc[0] + self.settingsButtonWidth, self.flipBoardLoc[1], self.settingsButtonWidth, self.settingsButtonHeight))
        flipBoardOffText = TEXT_FONT.render("Disabled", 0, TEXT_COLOR)
        self.screen.blit(flipBoardLabel, (self.flipBoardLoc[0] + (((2 * self.settingsButtonWidth) - flipBoardLabel.get_width()) / 2), self.flipBoardLoc[1] - (1.5 * flipBoardLabel.get_height())))
        self.screen.blit(flipBoardOnText, (self.flipBoardLoc[0] + ((self.settingsButtonWidth - flipBoardOnText.get_width()) / 2), self.flipBoardLoc[1] + ((self.settingsButtonHeight - flipBoardOnText.get_height()) / 2)))
        self.screen.blit(flipBoardOffText, (self.flipBoardLoc[0] + self.settingsButtonWidth + ((self.settingsButtonWidth - flipBoardOffText.get_width()) / 2), self.flipBoardLoc[1] + ((self.settingsButtonHeight - flipBoardOffText.get_height()) / 2)))

        #draw Clock Time Change buttons
        changeTimeLabel = LABEL_FONT.render("Current time: " + str(ss.clockLength) + "+" + str(ss.clockIncrement), 0, LABEL_COLOR)
        p.draw.rect(self.screen, p.Color("black"), p.Rect(self.baseTimeLoc[0], self.baseTimeLoc[1], 2 * self.settingsButtonWidth, self.settingsButtonHeight))
        changeBaseTimeText = TEXT_FONT.render("Change Base Time", 0, TEXT_COLOR)
        p.draw.rect(self.screen, p.Color("black"), p.Rect(self.incrementTimeLoc[0], self.incrementTimeLoc[1], 2 * self.settingsButtonWidth, self.settingsButtonHeight))
        changeIncrementTimeText = TEXT_FONT.render("Change Increment Time", 0, TEXT_COLOR)
        self.screen.blit(changeTimeLabel, ((self.WINDOW_WIDTH - changeTimeLabel.get_width()) / 2, self.baseTimeLoc[1] - (1.5 * changeTimeLabel.get_height())))
        self.screen.blit(changeBaseTimeText, (self.baseTimeLoc[0] + (((2 * self.settingsButtonWidth) - changeBaseTimeText.get_width()) / 2), self.baseTimeLoc[1] + ((self.settingsButtonHeight - changeBaseTimeText.get_height()) / 2)))
        self.screen.blit(changeIncrementTimeText, (self.incrementTimeLoc[0] + (((2 * self.settingsButtonWidth) - changeIncrementTimeText.get_width()) / 2), self.incrementTimeLoc[1] + ((self.settingsButtonHeight - changeIncrementTimeText.get_height()) / 2)))

    def getSettingButtonColor(self, ss, setting, state):
        SELECTED_COLOR = p.Color("black")
        UNSELECTED_COLOR = p.Color("gray")

        if setting == "boardColorScheme":
            if (state == "coffee") & (ss.boardColorScheme == "coffee"):
                return SELECTED_COLOR
            elif (state == "greyscale") & (ss.boardColorScheme == "greyscale"):
                return SELECTED_COLOR
            else:
                return UNSELECTED_COLOR
        elif setting == "moveHighlighting":
            if ((state == "on") & (ss.highlightValidMoves == True)) | ((state == "off") & (ss.highlightValidMoves == False)):
                return SELECTED_COLOR
            else:
                return UNSELECTED_COLOR
        elif setting == "autoQueen":
            if ((state == "on") & (ss.autoQueen == True)) | ((state == "off") & (ss.autoQueen == False)):
                return SELECTED_COLOR
            else:
                return UNSELECTED_COLOR
        elif setting == "pieceStyle":
            if (state == "standard") & (ss.pieceStyle == "standard"):
                return SELECTED_COLOR
            elif (state == "leipzig") & (ss.pieceStyle == "leipzig"):
                return SELECTED_COLOR
            else:
                return UNSELECTED_COLOR
        elif setting == "undoMove":
            if ((state == "on") & (ss.undoMoveEnabled == True)) | ((state == "off") & (ss.undoMoveEnabled == False)):
                return SELECTED_COLOR
            else:
                return UNSELECTED_COLOR
        elif setting == "flipBoard":
            if ((state == "on") & (ss.flipBoard == True)) | ((state == "off") & (ss.flipBoard == False)):
                return SELECTED_COLOR
            else:
                return UNSELECTED_COLOR

    def checkBackButtonPressed(self):
        if (self.backLoc[0] < p.mouse.get_pos()[0] < (self.backLoc[0] + self.settingsButtonWidth)) & (self.backLoc[1] < p.mouse.get_pos()[1] < (self.backLoc[1] + self.settingsButtonHeight)):
            self.backButton = True

    def changeBaseTime(self, ss):
        while True:
            new_time = input("Enter a new base time (minutes): ")
            new_time = float(new_time)
            new_time = int(new_time)
            if type(new_time) is int:
                if (new_time >= 1) & (new_time <= 180):
                    ss.clockLength = new_time
                    break
            else:
                print("Provided base time is invalid.")

    def changeIncrementTime(self, ss):
        while True:
            new_time = input("Enter a new increment time (seconds): ")
            new_time = int(new_time)
            if type(new_time) is int:
                if (new_time >= 0) & (new_time <= 120):
                    ss.clockIncrement = new_time
                    break
            else:
                print("Provided increment time is invalid.")

    def evaluateSettingsChanges(self, ss):
        x = p.mouse.get_pos()[0]
        y = p.mouse.get_pos()[1]
        if (x > self.boardColorSchemeLoc[0]) & (x < self.boardColorSchemeLoc[0] + (2 * self.settingsButtonWidth)) & (y > self.boardColorSchemeLoc[1]) & (y < self.boardColorSchemeLoc[1] + self.settingsButtonHeight):
            if x < (self.boardColorSchemeLoc[0] + self.settingsButtonWidth):
                ss.boardColorScheme = "coffee"
            else:
                ss.boardColorScheme = "greyscale"
        if (x > self.moveHighlightingLoc[0]) & (x < self.moveHighlightingLoc[0] + (2 * self.settingsButtonWidth)) & (y > self.moveHighlightingLoc[1]) & (y < self.moveHighlightingLoc[1] + self.settingsButtonHeight):
            if x < (self.moveHighlightingLoc[0] + self.settingsButtonWidth):
                ss.highlightValidMoves = True
            else:
                ss.highlightValidMoves = False
        if (x > self.autoQueenLoc[0]) & (x < self.autoQueenLoc[0] + (2 * self.settingsButtonWidth)) & (y > self.autoQueenLoc[1]) & (y < self.autoQueenLoc[1] + self.settingsButtonHeight):
            if x < (self.autoQueenLoc[0] + self.settingsButtonWidth):
                ss.autoQueen = True
            else:
                ss.autoQueen = False
        if (x > self.pieceStyleLoc[0]) & (x < self.pieceStyleLoc[0] + (2 * self.settingsButtonWidth)) & (y > self.pieceStyleLoc[1]) & (y < self.pieceStyleLoc[1] + self.settingsButtonHeight):
            if x < (self.pieceStyleLoc[0] + self.settingsButtonWidth):
                ss.pieceStyle = "standard"
            else:
                ss.pieceStyle = "leipzig"
        if (x > self.undoMoveLoc[0]) & (x < self.undoMoveLoc[0] + (2 * self.settingsButtonWidth)) & (y > self.undoMoveLoc[1]) & (y < self.undoMoveLoc[1] + self.settingsButtonHeight):
            if x < (self.undoMoveLoc[0] + self.settingsButtonWidth):
                ss.undoMoveEnabled = True
            else:
                ss.undoMoveEnabled = False
        if (x > self.flipBoardLoc[0]) & (x < self.flipBoardLoc[0] + (2 * self.settingsButtonWidth)) & (y > self.flipBoardLoc[1]) & (y < self.flipBoardLoc[1] + self.settingsButtonHeight):
            if x < (self.flipBoardLoc[0] + self.settingsButtonWidth):
                ss.flipBoard = True
            else:
                ss.flipBoard = False
        if (x > self.baseTimeLoc[0]) & (x < self.baseTimeLoc[0] + (2 * self.settingsButtonWidth)) & (y > self.baseTimeLoc[1]) & (y < self.baseTimeLoc[1] + self.settingsButtonHeight):
            self.changeBaseTime(ss)
        if (x > self.incrementTimeLoc[0]) & (x < self.incrementTimeLoc[0] + (2 * self.settingsButtonWidth)) & (y > self.incrementTimeLoc[1]) & (y < self.incrementTimeLoc[1] + self.settingsButtonHeight):
            self.changeIncrementTime(ss)


    def fillScreenWithWhite(self):
        self.screen.fill(p.Color("white"))

    def tickClock(self, FPS = None):
        if FPS == None:
            FPS = self.FPS
        self.clock.tick(FPS)

    def flipDisplay(self):
        p.display.flip()