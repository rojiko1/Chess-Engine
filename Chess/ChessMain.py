import pygame as p

from Chess import ChessEngine
from Chess import OtherStates

#Project status: draw by repetition, 50 move rule yet to do, lichess api, chess notation

WINDOW_WIDTH = 1280 #1280, 960, 640
WINDOW_HEIGHT = 800 #800, 600, 400
WIDTH = HEIGHT = 800 #800, 600, 400
DIMENSION = 8
SQ_SIZE = HEIGHT / DIMENSION
FPS = 30
IMAGES = []
PIECES = ["bR", "bN", "bB", "bQ", "bK", "bp", "wp", "wR", "wN", "wB", "wQ", "wK"]
BOARD_COLORS = {"coffee": [p.Color("burlywood"), p.Color("salmon4")], "greyscale": [p.Color("gray90"), p.Color("gray60")]}
turnLabel = "White's"

def loadImages(pieceStyle):
    #load standard pieces part 1
    stanPieces = OtherStates.SpriteSheet(p.image.load("images/standardpieces.png"), 2, 6)
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
        #load standard pieces part 2
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
        IMAGES.append(p.transform.scale(p.image.load("images/leipzigPieces/leipzig" + piece +".png"), (SQ_SIZE, SQ_SIZE))) #load leipzig pieces

    IMAGES.append(p.transform.scale(p.image.load("images/cover.png"), (1563 / (2560 / WINDOW_WIDTH), 1042 / (1600 / WINDOW_HEIGHT))))
    IMAGES.append(p.transform.scale(p.image.load("images/reddot.png"), (SQ_SIZE, SQ_SIZE)))
    IMAGES.append(p.transform.scale(p.image.load("images/dot.png"), (SQ_SIZE, SQ_SIZE)))
    IMAGES.append(p.transform.scale(p.image.load("images/target.png"), (SQ_SIZE, SQ_SIZE)))

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
    menu_complete = run_menu(screen, clock, ms, ss, running) #runs menu and waits for something to be returned
    if menu_complete:
        #game screen
        sqSelected = ()
        playerClicks = []
        moveMade = False
        p.display.flip()
        legalMoves = gs.getLegalMoves()
        while running:
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif (e.type == p.MOUSEBUTTONDOWN) & (p.mouse.get_pos()[0] < WIDTH) & (p.mouse.get_pos()[1] < HEIGHT):
                    location = p.mouse.get_pos()
                    column = location[0] / SQ_SIZE
                    row = location[1] / SQ_SIZE
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
                                        print("q for queen")
                                        print("n or k for knight")
                                        print("r for rook")
                                        print("b for bishop")
                                        choice = input("Choose a piece to promote to: ")
                                        if (choice == "q") | (choice == "Q"):
                                            legalMove.promotionChoice = "Q"
                                        if (choice == "n") | (choice == "N") | (choice == "k") | (choice == "K"):
                                            legalMove.promotionChoice = "N"
                                        if (choice == "r") | (choice == "R"):
                                            legalMove.promotionChoice = "R"
                                        if (choice == "b") | (choice == "B"):
                                            legalMove.promotionChoice = "B"
                                    gs.makeMove(legalMove)
                                    moveMade = True
                                    sqSelected = ()
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_BACKSPACE:
                        if ss.undoMoveEnabled:
                            gs.undoMove()
                            moveMade = True
            if moveMade:
                legalMoves = gs.getLegalMoves()
                moveMade = False
            drawGameState(screen, gs, ss, sqSelected, legalMoves)
            clock.tick(FPS)
            p.display.flip()

def run_menu(screen, clock, ms, ss, running):
    screen.fill(p.Color("white"))
    p.display.flip()
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                return False
            elif (e.type == p.MOUSEBUTTONDOWN) \
                    & (p.mouse.get_pos()[0] < WINDOW_WIDTH) & (p.mouse.get_pos()[1] < WINDOW_HEIGHT):
                ms.checkStartButtonPressed()
                ms.checkSettingsButtonPressed()
                if ms.startButton:
                    defaultSettings = open("defaultSettings.txt", "w")
                    defaultSettings.write(ss.boardColorScheme + "\n" + str(ss.highlightValidMoves) + "\n" + str(ss.autoQueen) + "\n" + ss.pieceStyle + "\n" + str(ss.undoMoveEnabled))
                    defaultSettings.close()
                    return True
                elif ms.settingsButton:
                    ms.settingsButton = False
                    settings_complete = run_settings(screen, clock, ss, running)
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

def drawMenuState(screen, ms):
    screen.fill(p.Color("white"))
    buttonWidth = ms.buttonWidth
    buttonHeight = ms.buttonHeight
    startLoc = ms.startButtonLocation
    settingsLoc = ms.settingsButtonLocation
    TEXT_FONT = p.font.SysFont('calibri', int(WINDOW_WIDTH * (32 / 1280)), False, False)
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
    buttonStartX = ss.buttonStartX
    textStartX = ss.textStartX
    backLoc = ss.backButtonLocation
    #flipBoardLoc = ss.flipBoardLocation
    boardColorSchemeLoc = ss.boardColorSchemeLocation
    moveHighlightingLoc = ss.moveHighlightingLocation
    autoQueenLoc = ss.autoQueenLocation
    pieceStyleLoc = ss.pieceStyleLocation
    undoMoveLoc = ss.undoMoveLocation

    TITLE_TEXT_FONT = p.font.SysFont('calibri', int(WINDOW_WIDTH * (88 / 1280)), True, False)
    TITLE_TEXT_COLOR = p.Color("black")
    LABEL_FONT = p.font.SysFont('calibri', int(WINDOW_WIDTH * (44 / 1280)), False, False)
    LABEL_COLOR = p.Color("black")
    TEXT_FONT = p.font.SysFont('calibri', int(WINDOW_WIDTH * (32 / 1280)), False, False)
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

def drawGameState(screen, gs, ss, sqSelected, legalMoves):
    screen.fill(p.Color("white"))
    drawBoard(screen, gs, ss, sqSelected, legalMoves)
    drawPieces(screen, gs.board, ss.pieceStyle)
    renderMoveHistory(screen, gs)
    #showTurn(screen, gs)

def drawBoard(screen, gs, ss, sqSelected, legalMoves):
    colors = BOARD_COLORS[ss.boardColorScheme]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            p.draw.rect(screen, colors[(r + c) % 2], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if ss.highlightValidMoves:
        drawSelected(screen, gs, sqSelected, legalMoves)
    if gs.inCheck("w"):
        screen.blit(IMAGES[-3], p.Rect(gs.wKingLocation[1] * SQ_SIZE, gs.wKingLocation[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if gs.inCheck("b"):
        screen.blit(IMAGES[-3], p.Rect(gs.bKingLocation[1] * SQ_SIZE, gs.bKingLocation[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board, pieceStyle):
    if pieceStyle == "standard":
        constant = 0
    elif pieceStyle == "leipzig":
        constant = 1
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
               screen.blit(IMAGES[(2 * PIECES.index(piece)) + constant], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawSelected(screen, gs, sqSelected, legalMoves):
    if (len(sqSelected) > 0):
        if gs.board[int(sqSelected[0])][int(sqSelected[1])][0] == gs.getTurnColor():
            p.draw.rect(screen, p.Color("palegreen4"), p.Rect(int(sqSelected[1]) * SQ_SIZE, int(sqSelected[0]) * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            for move in legalMoves:
                if (move.startR == int(sqSelected[0])) & (move.startC == int(sqSelected[1])):
                    if move.pieceCaptured == "--":
                        screen.blit(IMAGES[-2], p.Rect(move.endC * SQ_SIZE, move.endR * SQ_SIZE, SQ_SIZE, SQ_SIZE))
                    elif (gs.whiteToMove & (move.pieceCaptured[0] == "b")) | ((not gs.whiteToMove) & (move.pieceCaptured[0] == "w")):
                        screen.blit(IMAGES[-1], p.Rect(move.endC * SQ_SIZE, move.endR * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def renderMoveHistory(screen, gs):
    TEXT_FONT = p.font.SysFont('calibri', int(WINDOW_WIDTH * (28 / 1280)), False, False)
    TEXTBOX_X = WIDTH
    TEXTBOX_Y = 0
    TEXTBOX_WIDTH = int(WINDOW_WIDTH - WIDTH)
    TEXTBOX_HEIGHT = HEIGHT
    TEXT_COLOR = p.Color("black")
    TEXTBOX_COLOR = p.Color("light gray")
    moveLogText = []
    p.draw.rect(screen, TEXTBOX_COLOR, p.Rect(TEXTBOX_X, TEXTBOX_Y, TEXTBOX_WIDTH, TEXTBOX_HEIGHT))
    for item in gs.moveLog:
        moveLogText.append(item.notation + ",")
    '''for item in gs.chessNotationLog:
        moveLogText.append(item + ",")'''
    if len(moveLogText) > 0:
        moveLogText[-1] = (moveLogText[-1])[:-1]
    space = TEXT_FONT.size(" ")[0]
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

def showTurn(screen, gs):
    TEXT_SIZE = WINDOW_WIDTH * (28 / 1280)
    TEXT_FONT = p.font.SysFont('calibri', TEXT_SIZE, True, False)
    TEXTBOX_X = 10
    TEXTBOX_Y = HEIGHT + 10
    TEXT_COLOR = p.Color("black")
    if gs.whiteToMove:
        turnLabel = "White's"
    else:
        turnLabel = "Black's"
    turn_screen = TEXT_FONT.render(turnLabel, 0, TEXT_COLOR)
    turn_screen2 = TEXT_FONT.render("Turn", 0, TEXT_COLOR)
    turn_rect = turn_screen.get_rect(center = ((WIDTH + WINDOW_WIDTH) / 2, ((HEIGHT + WINDOW_HEIGHT) / 2) - (TEXT_SIZE / 2)))
    turn_rect2 = turn_screen2.get_rect(center = ((WIDTH + WINDOW_WIDTH) / 2, ((HEIGHT + WINDOW_HEIGHT) / 2) + (TEXT_SIZE / 2)))
    screen.blit(turn_screen, turn_rect)
    screen.blit(turn_screen2, turn_rect2)

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
    if setting == "moveHighlighting":
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

main()