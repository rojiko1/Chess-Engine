import pygame as p

from Chess.src.Engine import ChessEngine
from Chess.src.OtherStates import OtherStates
from Chess.src.Server import Network

#Project status: drag pieces to make move, multiplayer w/ server, lichess api, chess notation
#Current issue:

SIZE_MULTIPLIER = 2 #suggested (in order of largest to smallest window size): 2, 8/3, 4
WINDOW_WIDTH = 2560 / SIZE_MULTIPLIER
WINDOW_HEIGHT = 1800 / SIZE_MULTIPLIER
WIDTH = HEIGHT = 1600 / SIZE_MULTIPLIER
DIMENSION = 8
SQ_SIZE = HEIGHT / DIMENSION
FPS = 30
IMAGES = [] #once populated, indices 0-23: pieces alternating between standard and leipzig, 24-27: cover, red in-check dot, green possible-move dot, possible-capture target
PIECES = ["bR", "bN", "bB", "bQ", "bK", "bp", "wp", "wR", "wN", "wB", "wQ", "wK"]
BOARD_COLORS = {"coffee": [p.Color("burlywood"), p.Color("salmon4")], "greyscale": [p.Color("gray90"), p.Color("gray60")]}

def loadImages(pieceStyle):
    #load spritesheet of standard pieces
    stanPieces = OtherStates.SpriteSheet(p.image.load("../../images/standardpieces.png"), 2, 6)
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
    for piece in PIECES:
        #scale subimages and add to IMAGES array
        if piece[0] == "b":
            if piece[1] == "K":
                IMAGES.append(p.transform.scale(standardbK, (SQ_SIZE, SQ_SIZE)))
            elif piece[1] == "Q":
                IMAGES.append(p.transform.scale(standardbQ, (SQ_SIZE, SQ_SIZE)))
            elif piece[1] == "R":
                IMAGES.append(p.transform.scale(standardbR, (SQ_SIZE, SQ_SIZE)))
            elif piece[1] == "B":
                IMAGES.append(p.transform.scale(standardbB, (SQ_SIZE, SQ_SIZE)))
            elif piece[1] == "N":
                IMAGES.append(p.transform.scale(standardbN, (SQ_SIZE, SQ_SIZE)))
            elif piece[1] == "p":
                IMAGES.append(p.transform.scale(standardbp, (SQ_SIZE, SQ_SIZE)))
        elif piece[0] == "w":
            if piece[1] == "K":
                IMAGES.append(p.transform.scale(standardwK, (SQ_SIZE, SQ_SIZE)))
            elif piece[1] == "Q":
                IMAGES.append(p.transform.scale(standardwQ, (SQ_SIZE, SQ_SIZE)))
            elif piece[1] == "R":
                IMAGES.append(p.transform.scale(standardwR, (SQ_SIZE, SQ_SIZE)))
            elif piece[1] == "B":
                IMAGES.append(p.transform.scale(standardwB, (SQ_SIZE, SQ_SIZE)))
            elif piece[1] == "N":
                IMAGES.append(p.transform.scale(standardwN, (SQ_SIZE, SQ_SIZE)))
            elif piece[1] == "p":
                IMAGES.append(p.transform.scale(standardwp, (SQ_SIZE, SQ_SIZE)))
        #for all pieces in PIECES array, load and add corresponding leipzig piece to IMAGES array
        IMAGES.append(p.transform.scale(p.image.load("../../images/leipzigPieces/leipzig" + piece +".png"), (SQ_SIZE, SQ_SIZE))) #load leipzig pieces

    #load and add other non-piece images to IMAGES array
    IMAGES.append(p.transform.scale(p.image.load("../../images/cover.png"), (1563 / (2560 / WINDOW_WIDTH), 1042 / (1800 / WINDOW_HEIGHT))))
    IMAGES.append(p.transform.scale(p.image.load("../../images/reddot.png"), (SQ_SIZE, SQ_SIZE)))
    IMAGES.append(p.transform.scale(p.image.load("../../images/dot.png"), (SQ_SIZE, SQ_SIZE)))
    IMAGES.append(p.transform.scale(p.image.load("../../images/target.png"), (SQ_SIZE, SQ_SIZE)))

def main():
    p.init()
    screen = p.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    screen.fill(p.Color("white"))
    p.display.set_caption("Chess Engine")
    clock = p.time.Clock()
    ms = OtherStates.MenuState(WINDOW_WIDTH, WINDOW_HEIGHT)
    ss = OtherStates.SettingsState(WINDOW_WIDTH, WINDOW_HEIGHT)
    gs = ChessEngine.GameState()
    loadImages(ss.pieceStyle)
    running = True
    menu_complete = run_menu(screen, clock, ms, ss, running) #runs menu loop and waits for cue to start game or close window
    if menu_complete:
        #game screen
        #n = Network.Network()
        #startPos = n.getPos()
        gameClock = ChessEngine.Clock(ss.clockLength, ss.clockIncrement, ss.clockLength, ss.clockIncrement)
        whiteClockOn = True
        num_ticks = 0
        gameComplete = False
        sqSelected = ()
        playerClicks = []
        moveMade = False
        tempFiftyMove = False
        tempRepetition = False
        tempInsufficientMaterial = False
        whiteTimeout = False
        blackTimeout = False
        p.display.flip()
        legalMoves = gs.getLegalMoves()
        #game loop
        while running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif (e.type == p.MOUSEBUTTONDOWN) & (p.mouse.get_pos()[0] < WIDTH) & (p.mouse.get_pos()[1] < HEIGHT) & (not gameComplete):
                    location = p.mouse.get_pos()
                    column = int(location[0] / SQ_SIZE)
                    row = adjustForFlipBoard(int(location[1] / SQ_SIZE), gs.whiteToMove, ss.flipBoard)
                    if sqSelected == (row, column):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, column)
                        playerClicks.append(sqSelected)
                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            for legalMove in legalMoves:
                                if move == legalMove:
                                    if (legalMove.pawnPromotion) & (not ss.autoQueen):
                                        choiceMade = False
                                        print("q for queen")
                                        print("n or k for knight")
                                        print("r for rook")
                                        print("b for bishop")
                                        while not choiceMade:
                                            choice = p.event.wait()
                                            if (choice.type == p.KEYDOWN):
                                                if choice.key == p.K_q:
                                                    legalMove.promotionChoice = "Q"
                                                    choiceMade = True
                                                elif (choice.key == p.K_n) | (choice.key == p.K_k):
                                                    legalMove.promotionChoice = "N"
                                                    choiceMade = True
                                                elif choice.key == p.K_r:
                                                    legalMove.promotionChoice = "R"
                                                    choiceMade = True
                                                elif choice.key == p.K_b:
                                                    legalMove.promotionChoice = "B"
                                                    choiceMade = True
                                    gs.makeMove(legalMove)
                                    tempFiftyMove = gs.fiftyMoveRuleDraw
                                    tempRepetition = gs.drawByRepetition
                                    tempInsufficientMaterial = gs.insufficientMaterial
                                    moveMade = True
                                    sqSelected = ()
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]
                elif (e.type == p.KEYDOWN) & (not gameComplete):
                    if e.key == p.K_BACKSPACE:
                        if (ss.undoMoveEnabled) & (len(gs.moveLog) > 0):
                            gameClock.decrement(gs.getTurnColor()) #prevents time gain from undoing a move
                            gs.undoMove()
                            moveMade = True
                    if e.key == p.K_x: #reset gameState
                        gs.resetGameState()
                        gameClock.resetClock(ss.clockLength, ss.clockIncrement, ss.clockLength, ss.clockIncrement)
                        whiteClockOn = True
                        num_ticks = 0
                        gameComplete = False
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        tempFiftyMove = False
                        tempRepetition = False
                        tempInsufficientMaterial = False
                        whiteTimeout = False
                        blackTimeout = False
                        legalMoves = gs.getLegalMoves()
            if moveMade:
                gameClock.increment(gs.getOppColor(gs.getTurnColor()))
                whiteClockOn = not whiteClockOn
                num_ticks = 0
                animateMove(screen, gs, ss, clock)
                legalMoves = gs.getLegalMoves()
                moveMade = False
            if not gameComplete:
                if len(gs.moveLog) > 0:
                    num_ticks = num_ticks + 1
                    if(num_ticks >= FPS):
                        gameClock.updateClock(gs.getTurnColor())
                        num_ticks = 0
                        if gameClock.whiteBaseTime == 0:
                            whiteTimeout = True
                        elif gameClock.blackBaseTime == 0:
                            blackTimeout = True
                drawGameState(screen, gs, ss, sqSelected, legalMoves, gameClock, whiteClockOn)
                if gs.checkmate:
                    gameComplete = True
                    drawEndOfGame(screen, "checkmate", color = gs.getOppColor(gs.getTurnColor()))
                elif gs.stalemate:
                    gameComplete = True
                    drawEndOfGame(screen, "stalemate")
                elif tempInsufficientMaterial:
                    gameComplete = True
                    drawEndOfGame(screen, "insufficientMaterial")
                elif tempRepetition:
                    gameComplete = True
                    drawEndOfGame(screen, "repetition")
                elif tempFiftyMove:
                    gameComplete = True
                    drawEndOfGame(screen, "fiftyMove")
                elif whiteTimeout:
                    gameComplete = True
                    drawEndOfGame(screen, "whiteTimeout")
                elif blackTimeout:
                    gameComplete = True
                    drawEndOfGame(screen, "blackTimeout")
            clock.tick(FPS)
            p.display.flip()

def run_menu(screen, clock, ms, ss, running):
    screen.fill(p.Color("white"))
    p.display.flip()
    printGameInstructions()
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                return False
            elif (e.type == p.MOUSEBUTTONDOWN) \
                    & (p.mouse.get_pos()[0] < WINDOW_WIDTH) & (p.mouse.get_pos()[1] < WINDOW_HEIGHT):
                ms.checkStartButtonPressed()
                ms.checkSettingsButtonPressed()
                if ms.startButton:
                    defaultSettings = open("../defaultSettings.txt", "w")
                    defaultSettings.write(ss.boardColorScheme + "\n" + str(ss.highlightValidMoves) + "\n" + str(ss.autoQueen) + "\n" + ss.pieceStyle + "\n" + str(ss.undoMoveEnabled) + "\n" + str(ss.flipBoard))
                    defaultSettings.close()
                    return True
                elif ms.settingsButton:
                    ms.settingsButton = False
                    settings_complete = run_settings(screen, clock, ss, running) #runs settings loop and waits for cue to return to menu or close window
                    if not settings_complete:
                        return False
        drawMenuState(screen, ms)
        clock.tick(FPS)
        p.display.flip()

def run_settings(screen, clock, ss, running):
    screen.fill(p.Color("white"))
    p.display.flip()
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                return False
            elif (e.type == p.MOUSEBUTTONDOWN) \
                    & (p.mouse.get_pos()[0] < WINDOW_WIDTH) & (p.mouse.get_pos()[1] < WINDOW_HEIGHT):
                ss.checkBackButtonPressed()
                ss.evaluateSettingsChanges()
                if ss.backButton:
                    ss.backButton = False
                    return True
        drawSettingsState(screen, ss)
        clock.tick(FPS)
        p.display.flip()

def printGameInstructions():
    print(" ")
    print("Hello and welcome to Rohil's chess engine!")
    print("Adjust your settings or start a game.")
    print("Here are some keyboard controls you should know:")
    print("If you have auto queen disabled, when promoting a pawn, use the 'q', 'r', 'n', and 'b' keys to make your promotion choice.")
    print("If you have undo move enabled, use the 'backspace' key to undo a move.")
    print("To reset the game at any time, press the 'x' key.")
    print("Good luck player and feel free to leave feedback!")
    print(" ")

def drawMenuState(screen, ms):
    screen.fill(p.Color("white"))
    buttonWidth = ms.buttonWidth
    buttonHeight = ms.buttonHeight
    startLoc = ms.startButtonLocation
    settingsLoc = ms.settingsButtonLocation
    TEXT_FONT = p.font.SysFont('arial', int(WINDOW_WIDTH * (28 / 1280)), False, False)
    TEXT_COLOR = p.Color("white")
    buttonColor = p.Color("black")

    #draw Start button
    p.draw.rect(screen, "black", p.Rect(startLoc[0], startLoc[1], buttonWidth, buttonHeight))
    startText = TEXT_FONT.render("Start", 0, TEXT_COLOR)
    screen.blit(startText, (startLoc[0] + ((buttonWidth - startText.get_width()) / 2), startLoc[1] + ((buttonHeight - startText.get_height()) / 2)))

    #draw Settings button
    p.draw.rect(screen, "black", p.Rect(settingsLoc[0], settingsLoc[1], buttonWidth, buttonHeight))
    settingsText = TEXT_FONT.render("Settings", 0, TEXT_COLOR)
    screen.blit(settingsText, (settingsLoc[0] + ((buttonWidth - settingsText.get_width()) / 2), settingsLoc[1] + ((buttonHeight - settingsText.get_height()) / 2)))

    screen.blit(IMAGES[-4], p.Rect((WINDOW_WIDTH - IMAGES[-4].get_width()) / 2, (startLoc[1] - IMAGES[-4].get_height()) / 2, IMAGES[-4].get_width(), IMAGES[-4].get_height()))

def drawSettingsState(screen, ss):
    screen.fill(p.Color("white"))
    buttonWidth = ss.buttonWidth
    buttonHeight = ss.buttonHeight
    backLoc = ss.backButtonLocation
    boardColorSchemeLoc = ss.boardColorSchemeLocation
    moveHighlightingLoc = ss.moveHighlightingLocation
    autoQueenLoc = ss.autoQueenLocation
    pieceStyleLoc = ss.pieceStyleLocation
    undoMoveLoc = ss.undoMoveLocation
    flipBoardLoc = ss.flipBoardLocation

    TITLE_TEXT_FONT = p.font.SysFont('arial', int(WINDOW_WIDTH * (80 / 1280)), True, False)
    TITLE_TEXT_COLOR = p.Color("black")
    LABEL_FONT = p.font.SysFont('arial', int(WINDOW_WIDTH * (40 / 1280)), False, False)
    LABEL_COLOR = p.Color("black")
    TEXT_FONT = p.font.SysFont('arial', int(WINDOW_WIDTH * (28 / 1280)), False, False)
    TEXT_COLOR = p.Color("white")

    titleText = TITLE_TEXT_FONT.render("SETTINGS", 0, TITLE_TEXT_COLOR)
    screen.blit(titleText, ((WINDOW_WIDTH - titleText.get_width()) / 2, WINDOW_HEIGHT / 20))

    #draw Back button
    p.draw.rect(screen, p.Color("firebrick1"), p.Rect(backLoc[0], backLoc[1], buttonWidth, buttonHeight))
    backText = TEXT_FONT.render("Back", 0, TEXT_COLOR)
    screen.blit(backText, (backLoc[0] + ((buttonWidth - backText.get_width()) / 2), backLoc[1] + ((buttonHeight - backText.get_height()) / 2)))

    #draw Board Color Scheme Settings buttons
    boardColorSchemeLabel = LABEL_FONT.render("Board Color Scheme", 0, LABEL_COLOR)
    p.draw.rect(screen, getSettingButtonColor(ss, "boardColorScheme", "coffee"), p.Rect(boardColorSchemeLoc[0], boardColorSchemeLoc[1], buttonWidth, buttonHeight))
    boardColorCoffeeText = TEXT_FONT.render("Coffee", 0, TEXT_COLOR)
    p.draw.rect(screen, getSettingButtonColor(ss, "boardColorScheme", "greyscale"), p.Rect(boardColorSchemeLoc[0] + buttonWidth, boardColorSchemeLoc[1], buttonWidth, buttonHeight))
    boardColorGreyscaleText = TEXT_FONT.render("Greyscale", 0, TEXT_COLOR)
    screen.blit(boardColorSchemeLabel, (boardColorSchemeLoc[0] + (((2 * buttonWidth) - boardColorSchemeLabel.get_width()) / 2), boardColorSchemeLoc[1] - (1.5 * boardColorSchemeLabel.get_height())))
    screen.blit(boardColorCoffeeText, (boardColorSchemeLoc[0] + ((buttonWidth - boardColorCoffeeText.get_width()) / 2), boardColorSchemeLoc[1] + ((buttonHeight - boardColorCoffeeText.get_height()) / 2)))
    screen.blit(boardColorGreyscaleText, (boardColorSchemeLoc[0] + buttonWidth + ((buttonWidth - boardColorGreyscaleText.get_width()) / 2), boardColorSchemeLoc[1] + ((buttonHeight - boardColorGreyscaleText.get_height()) / 2)))

    #draw Move Highlighting Settings buttons
    moveHighlightingLabel = LABEL_FONT.render("Move Highlighting", 0, LABEL_COLOR)
    p.draw.rect(screen, getSettingButtonColor(ss, "moveHighlighting", "on"), p.Rect(moveHighlightingLoc[0], moveHighlightingLoc[1], buttonWidth, buttonHeight))
    moveHighlightingOnText = TEXT_FONT.render("Enabled", 0, TEXT_COLOR)
    p.draw.rect(screen, getSettingButtonColor(ss, "moveHighlighting", "off"), p.Rect(moveHighlightingLoc[0] + buttonWidth, moveHighlightingLoc[1], buttonWidth, buttonHeight))
    moveHighlightingOffText = TEXT_FONT.render("Disabled", 0, TEXT_COLOR)
    screen.blit(moveHighlightingLabel, (moveHighlightingLoc[0] + (((2 * buttonWidth) - moveHighlightingLabel.get_width()) / 2), moveHighlightingLoc[1] - (1.5 * moveHighlightingLabel.get_height())))
    screen.blit(moveHighlightingOnText, (moveHighlightingLoc[0] + ((buttonWidth - moveHighlightingOnText.get_width()) / 2), moveHighlightingLoc[1] + ((buttonHeight - moveHighlightingOnText.get_height()) / 2)))
    screen.blit(moveHighlightingOffText, (moveHighlightingLoc[0] + buttonWidth + ((buttonWidth - moveHighlightingOffText.get_width()) / 2), moveHighlightingLoc[1] + ((buttonHeight - moveHighlightingOffText.get_height()) / 2)))

    #draw Auto Queen Settings buttons
    autoQueenLabel = LABEL_FONT.render("Auto Queen", 0, LABEL_COLOR)
    p.draw.rect(screen, getSettingButtonColor(ss, "autoQueen", "on"), p.Rect(autoQueenLoc[0], autoQueenLoc[1], buttonWidth, buttonHeight))
    autoQueenOnText = TEXT_FONT.render("Enabled", 0, TEXT_COLOR)
    p.draw.rect(screen, getSettingButtonColor(ss, "autoQueen", "off"), p.Rect(autoQueenLoc[0] + buttonWidth, autoQueenLoc[1], buttonWidth, buttonHeight))
    autoQueenOffText = TEXT_FONT.render("Disabled", 0, TEXT_COLOR)
    screen.blit(autoQueenLabel, (autoQueenLoc[0] + (((2 * buttonWidth) - autoQueenLabel.get_width()) / 2), autoQueenLoc[1] - (1.5 * autoQueenLabel.get_height())))
    screen.blit(autoQueenOnText, (autoQueenLoc[0] + ((buttonWidth - autoQueenOnText.get_width()) / 2), autoQueenLoc[1] + ((buttonHeight - autoQueenOnText.get_height()) / 2)))
    screen.blit(autoQueenOffText, (autoQueenLoc[0] + buttonWidth + ((buttonWidth - autoQueenOffText.get_width()) / 2), autoQueenLoc[1] + ((buttonHeight - autoQueenOffText.get_height()) / 2)))

    #draw Piece Style Settings buttons
    pieceStyleLabel = LABEL_FONT.render("Piece Style", 0, LABEL_COLOR)
    p.draw.rect(screen, getSettingButtonColor(ss, "pieceStyle", "standard"), p.Rect(pieceStyleLoc[0], pieceStyleLoc[1], buttonWidth, buttonHeight))
    standardPieceStyleText = TEXT_FONT.render("Standard", 0, TEXT_COLOR)
    p.draw.rect(screen, getSettingButtonColor(ss, "pieceStyle", "leipzig"), p.Rect(pieceStyleLoc[0] + buttonWidth, pieceStyleLoc[1], buttonWidth, buttonHeight))
    leipzigPieceStyleText = TEXT_FONT.render("Leipzig", 0, TEXT_COLOR)
    screen.blit(pieceStyleLabel, (pieceStyleLoc[0] + (((2 * buttonWidth) - pieceStyleLabel.get_width()) / 2), pieceStyleLoc[1] - (1.5 * pieceStyleLabel.get_height())))
    screen.blit(standardPieceStyleText, (pieceStyleLoc[0] + ((buttonWidth - standardPieceStyleText.get_width()) / 2), pieceStyleLoc[1] + ((buttonHeight - standardPieceStyleText.get_height()) / 2)))
    screen.blit(leipzigPieceStyleText, (pieceStyleLoc[0] + buttonWidth + ((buttonWidth - leipzigPieceStyleText.get_width()) / 2), pieceStyleLoc[1] + ((buttonHeight - leipzigPieceStyleText.get_height()) / 2)))

    #draw Undo Move Enabling Settings buttons
    undoMoveLabel = LABEL_FONT.render("Undo Move", 0, LABEL_COLOR)
    p.draw.rect(screen, getSettingButtonColor(ss, "undoMove", "on"), p.Rect(undoMoveLoc[0], undoMoveLoc[1], buttonWidth, buttonHeight))
    undoMoveOnText = TEXT_FONT.render("Enabled", 0, TEXT_COLOR)
    p.draw.rect(screen, getSettingButtonColor(ss, "undoMove", "off"), p.Rect(undoMoveLoc[0] + buttonWidth, undoMoveLoc[1], buttonWidth, buttonHeight))
    undoMoveOffText = TEXT_FONT.render("Disabled", 0, TEXT_COLOR)
    screen.blit(undoMoveLabel, (undoMoveLoc[0] + (((2 * buttonWidth) - undoMoveLabel.get_width()) / 2), undoMoveLoc[1] - (1.5 * undoMoveLabel.get_height())))
    screen.blit(undoMoveOnText, (undoMoveLoc[0] + ((buttonWidth - undoMoveOnText.get_width()) / 2), undoMoveLoc[1] + ((buttonHeight - undoMoveOnText.get_height()) / 2)))
    screen.blit(undoMoveOffText, (undoMoveLoc[0] + buttonWidth + ((buttonWidth - undoMoveOffText.get_width()) / 2), undoMoveLoc[1] + ((buttonHeight - undoMoveOffText.get_height()) / 2)))

    #draw Flip Board Enabling Settings buttons
    flipBoardLabel = LABEL_FONT.render("Flip Board", 0, LABEL_COLOR)
    p.draw.rect(screen, getSettingButtonColor(ss, "flipBoard", "on"), p.Rect(flipBoardLoc[0], flipBoardLoc[1], buttonWidth, buttonHeight))
    flipBoardOnText = TEXT_FONT.render("Enabled", 0, TEXT_COLOR)
    p.draw.rect(screen, getSettingButtonColor(ss, "flipBoard", "off"), p.Rect(flipBoardLoc[0] + buttonWidth, flipBoardLoc[1], buttonWidth, buttonHeight))
    flipBoardOffText = TEXT_FONT.render("Disabled", 0, TEXT_COLOR)
    screen.blit(flipBoardLabel, (flipBoardLoc[0] + (((2 * buttonWidth) - flipBoardLabel.get_width()) / 2), flipBoardLoc[1] - (1.5 * flipBoardLabel.get_height())))
    screen.blit(flipBoardOnText, (flipBoardLoc[0] + ((buttonWidth - flipBoardOnText.get_width()) / 2), flipBoardLoc[1] + ((buttonHeight - flipBoardOnText.get_height()) / 2)))
    screen.blit(flipBoardOffText, (flipBoardLoc[0] + buttonWidth + ((buttonWidth - flipBoardOffText.get_width()) / 2), flipBoardLoc[1] + ((buttonHeight - flipBoardOffText.get_height()) / 2)))

def drawEndOfGame(screen, state, color = "None"):
    TEXT_COLOR = p.Color("white")
    TEXT_FONT = p.font.SysFont('arial', int(WINDOW_WIDTH * (30 / 1280)), True, False)

    rectSize = (WIDTH / 2, HEIGHT / 10)
    rectPos = ((WIDTH - rectSize[0]) / 2, (HEIGHT - rectSize[1]) / 2)

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
    rectPos = ((WIDTH - rectSize[0]) / 2, (HEIGHT - rectSize[1]) / 2)
    rect = p.Surface(rectSize)
    rect.set_alpha(200) #set opacity
    rect.fill((0, 0, 0))
    screen.blit(rect, rectPos)

    screen.blit(text, (rectPos[0] + ((rectSize[0] - text.get_width()) / 2), rectPos[1] + ((rectSize[1] - text.get_height()) / 2)))

def drawGameState(screen, gs, ss, sqSelected, legalMoves, gameClock, whiteClockOn):
    screen.fill(p.Color("white"))
    drawBoard(screen, gs, ss)
    if ss.highlightValidMoves:
        drawSelected(screen, gs, ss, sqSelected, legalMoves)
    drawPieces(screen, gs, ss)
    renderMoveHistory(screen, gs)
    displayClock(screen, gameClock, whiteClockOn)

def drawBoard(screen, gs, ss):
    colors = BOARD_COLORS[ss.boardColorScheme]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            p.draw.rect(screen, colors[(adjustForFlipBoard(r, gs.whiteToMove, ss.flipBoard) + c) % 2], p.Rect(c * SQ_SIZE, adjustForFlipBoard(r, gs.whiteToMove, ss.flipBoard) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if gs.inCheck("w"):
        screen.blit(IMAGES[-3], p.Rect(gs.wKingLocation[1] * SQ_SIZE, gs.wKingLocation[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if gs.inCheck("b"):
        screen.blit(IMAGES[-3], p.Rect(gs.bKingLocation[1] * SQ_SIZE, adjustForFlipBoard(gs.bKingLocation[0], gs.whiteToMove, ss.flipBoard) * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, gs, ss):
    if ss.pieceStyle == "standard":
        constant = 0
    elif ss.pieceStyle == "leipzig":
        constant = 1
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = gs.board[r][c]
            if piece != "--":
                screen.blit(IMAGES[(2 * PIECES.index(piece)) + constant], p.Rect(c * SQ_SIZE, adjustForFlipBoard(r, gs.whiteToMove, ss.flipBoard) * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawSelected(screen, gs, ss, sqSelected, legalMoves):
    if (len(sqSelected) > 0):
        if gs.board[int(sqSelected[0])][int(sqSelected[1])][0] == gs.getTurnColor():
            p.draw.rect(screen, p.Color("palegreen4"), p.Rect(int(sqSelected[1]) * SQ_SIZE, adjustForFlipBoard(int(sqSelected[0]), gs.whiteToMove, ss.flipBoard) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            for move in legalMoves:
                if (move.startR == int(sqSelected[0])) & (move.startC == int(sqSelected[1])):
                    if move.pieceCaptured == "--":
                        screen.blit(IMAGES[-2], p.Rect(move.endC * SQ_SIZE, adjustForFlipBoard(move.endR, gs.whiteToMove, ss.flipBoard) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    elif (gs.whiteToMove & (move.pieceCaptured[0] == "b")) | ((not gs.whiteToMove) & (move.pieceCaptured[0] == "w")):
                        screen.blit(IMAGES[-1], p.Rect(move.endC * SQ_SIZE, adjustForFlipBoard(move.endR, gs.whiteToMove, ss.flipBoard) * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animateMove(screen, gs, ss, clock):
    frameCount = int(((ss.clockLength * 5) + (ss.clockIncrement * 10)) / 30) #num of frames over which animation occurs
    if (len(gs.moveLog) > 0) & (frameCount > 0):
        animationFPS = 60
        move = gs.moveLog[-1]
        delta_r = move.endR - move.startR
        delta_c = move.endC - move.startC
        if ss.pieceStyle == "standard":
            constant = 0
        elif ss.pieceStyle == "leipzig":
            constant = 1
        for frame in range(frameCount + 1):
            r, c = (move.startR + ((frame / frameCount) * delta_r), move.startC + ((frame / frameCount) * delta_c))
            #draw board and pieces
            drawBoard(screen, gs, ss)
            drawPieces(screen, gs, ss)
            #erase start and end squares
            startSquare = p.Rect(move.startC * SQ_SIZE, adjustForFlipBoard(move.startR, gs.whiteToMove, ss.flipBoard) * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, BOARD_COLORS[ss.boardColorScheme][(adjustForFlipBoard(move.startR, gs.whiteToMove, ss.flipBoard) + move.startC) % 2], startSquare)
            endSquare = p.Rect(move.endC * SQ_SIZE, adjustForFlipBoard(move.endR, gs.whiteToMove, ss.flipBoard) * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            p.draw.rect(screen, BOARD_COLORS[ss.boardColorScheme][(adjustForFlipBoard(move.endR, gs.whiteToMove, ss.flipBoard) + move.endC) % 2], endSquare)
            #if piece will be captured, redraw captured piece
            if move.pieceCaptured != "--":
                screen.blit(IMAGES[(2 * PIECES.index(move.pieceCaptured)) + constant], p.Rect(move.endC * SQ_SIZE, adjustForFlipBoard(move.endR, gs.whiteToMove, ss.flipBoard) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            #draw moved piece at animated coordinates
            screen.blit(IMAGES[(2 * PIECES.index(move.pieceMoved)) + constant], p.Rect(c * SQ_SIZE, adjustForFlipBoard(r, gs.whiteToMove, ss.flipBoard) * SQ_SIZE, SQ_SIZE, SQ_SIZE))

            p.display.flip()
            clock.tick(animationFPS)

def adjustForFlipBoard(row, whiteTurn, flipBoard):
    if flipBoard & (not whiteTurn):
        return abs(7 - row)
    else:
        return row

def renderMoveHistory(screen, gs):
    TEXT_FONT = p.font.SysFont('arial', int(WINDOW_WIDTH * (28 / 1280)), False, False)
    TEXTBOX_X = WIDTH
    TEXTBOX_Y = 0
    TEXTBOX_WIDTH = int(WINDOW_WIDTH - WIDTH)
    TEXTBOX_HEIGHT = HEIGHT
    TEXT_COLOR = p.Color("black")
    TEXTBOX_COLOR = p.Color("light gray")
    moveLogText = []
    space = TEXT_FONT.size(" ")[0]
    p.draw.rect(screen, TEXTBOX_COLOR, p.Rect(TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT))
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
        screen.blit(log_screen, (x, y))
        x += item_width + space #can remove space - stylistic choice

def displayClock(screen, gameClock, whiteClockOn):
    TEXT_FONT = p.font.SysFont('arial', int(WINDOW_WIDTH * (80 / 1280)), False, False)
    LABEL_FONT = p.font.SysFont('arial', int(WINDOW_WIDTH * (26 / 1280)), False, False)
    WHITE_CLOCK_X = 0
    BLACK_CLOCK_X = WINDOW_WIDTH / 2
    CLOCK_Y = HEIGHT
    CLOCK_WIDTH = WINDOW_WIDTH / 2
    CLOCK_HEIGHT = WINDOW_HEIGHT - HEIGHT
    TEXT_COLOR = p.Color("black")
    ON_COLOR = p.Color("olivedrab4")
    OFF_COLOR = p.Color("gray60")

    if whiteClockOn:
        whiteColor = ON_COLOR
        blackColor = OFF_COLOR
    else:
        whiteColor = OFF_COLOR
        blackColor = ON_COLOR

    #white clock
    p.draw.rect(screen, whiteColor, p.Rect(WHITE_CLOCK_X, CLOCK_Y, CLOCK_WIDTH, CLOCK_HEIGHT))
    white_hours = int(gameClock.whiteBaseTime / 3600)
    white_minutes = int((gameClock.whiteBaseTime - (white_hours * 3600)) / 60)
    white_seconds = int(gameClock.whiteBaseTime % 60)
    whiteTimeText = TEXT_FONT.render(str(white_hours) + ":" + str(white_minutes).zfill(2) + ":" + str(white_seconds).zfill(2), 0, TEXT_COLOR)
    screen.blit(whiteTimeText, (WHITE_CLOCK_X + ((CLOCK_WIDTH - whiteTimeText.get_width()) / 2), CLOCK_Y + ((CLOCK_HEIGHT - whiteTimeText.get_height()) / 2)))

    #black clock
    p.draw.rect(screen, blackColor, p.Rect(BLACK_CLOCK_X, CLOCK_Y, CLOCK_WIDTH, CLOCK_HEIGHT))
    black_hours = int(gameClock.blackBaseTime / 3600)
    black_minutes = int((gameClock.blackBaseTime - (black_hours * 3600)) / 60)
    black_seconds = int(gameClock.blackBaseTime % 60)
    blackTimeText = TEXT_FONT.render(str(black_hours) + ":" + str(black_minutes).zfill(2) + ":" + str(black_seconds).zfill(2), 0, TEXT_COLOR)
    screen.blit(blackTimeText, (BLACK_CLOCK_X + ((CLOCK_WIDTH - blackTimeText.get_width()) / 2), CLOCK_Y + ((CLOCK_HEIGHT - blackTimeText.get_height()) / 2)))

    #draw white rotated label
    whiteTimeLabel = LABEL_FONT.render("WHITE", 0, TEXT_COLOR)
    whiteTimeLabel = p.transform.rotate(whiteTimeLabel, 90)
    screen.blit(whiteTimeLabel, (WHITE_CLOCK_X + (0.1 * whiteTimeLabel.get_width()), CLOCK_Y + ((CLOCK_HEIGHT - whiteTimeLabel.get_height()) / 2)))

    #draw black rotated label
    blackTimeLabel = LABEL_FONT.render("BLACK", 0, TEXT_COLOR)
    blackTimeLabel = p.transform.rotate(blackTimeLabel, 90)
    screen.blit(blackTimeLabel, (BLACK_CLOCK_X + (0.1 * blackTimeLabel.get_width()), CLOCK_Y + ((CLOCK_HEIGHT - blackTimeLabel.get_height()) / 2)))

def getSettingButtonColor(ss, setting, state):
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

main()