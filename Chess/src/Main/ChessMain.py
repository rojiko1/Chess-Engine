import pygame as p

from Chess.src.Engine.Clock import Clock
from Chess.src.Engine.GameState import GameState
from Chess.src.Engine.Move import Move
from Chess.src.OtherStates.SettingsState import SettingsState
from Chess.src.UserInterface.UserInterface import UserInterface
from Chess.src.Server.Network import Network

#Project status: drag pieces to make move, scaling multiplayer w/ server, lichess api for AI, chess notation
#Current issue: start server from multiplayer, premove, end game communication

def main():
    ss = SettingsState()
    ui = UserInterface()
    running = True
    menu_complete = run_menu(ui, ss, running) #runs menu loop and waits for cue to start game or close window
    if menu_complete == False:
        running = False
    elif menu_complete == "oneMultiplayer":
        run_single_machine_multiplayer(ss, ui, running)
    elif menu_complete == "twoMultiplayer":
        run_two_machine_multiplayer(ss, ui, running)
    elif menu_complete == "singlePlayer":
        run_single_machine_multiplayer(ss, ui, running)

def run_menu(ui, ss, running):
    ui.fillScreenWithWhite()
    ui.flipDisplay()
    ui.printGameInstructions()
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                return False
            elif (e.type == p.MOUSEBUTTONDOWN) \
                    & (p.mouse.get_pos()[0] < ui.WINDOW_WIDTH) & (p.mouse.get_pos()[1] < ui.WINDOW_HEIGHT):
                ui.checkOneMultiplayerStartButtonPressed()
                ui.checkTwoMultiplayerStartButtonPressed()
                ui.checkSinglePlayerStartButtonPressed()
                ui.checkSettingsButtonPressed()
                if ui.oneMultiplayerStartButton:
                    defaultSettings = open("../defaultSettings.txt", "w")
                    defaultSettings.write(ss.boardColorScheme + "\n" + str(ss.highlightValidMoves) + "\n" + str(ss.autoQueen) + "\n" + ss.pieceStyle + "\n" + str(ss.undoMoveEnabled) + "\n" + str(ss.flipBoard) + "\n" + str(ss.clockLength) + "\n" + str(ss.clockIncrement))
                    defaultSettings.close()
                    return "oneMultiplayer"
                elif ui.twoMultiplayerStartButton:
                    return "twoMultiplayer"
                elif ui.singlePlayerStartButton:
                    defaultSettings = open("../defaultSettings.txt", "w")
                    defaultSettings.write(ss.boardColorScheme + "\n" + str(ss.highlightValidMoves) + "\n" + str(ss.autoQueen) + "\n" + ss.pieceStyle + "\n" + str(ss.undoMoveEnabled) + "\n" + str(ss.flipBoard) + "\n" + str(ss.clockLength) + "\n" + str(ss.clockIncrement))
                    defaultSettings.close()
                    return "singlePlayer"
                elif ui.settingsButton:
                    ui.settingsButton = False
                    settings_complete = run_settings(ui, ss, running) #runs settings loop and waits for cue to return to menu or close window
                    if not settings_complete:
                        return False
        ui.drawMenuState()
        ui.tickClock()
        ui.flipDisplay()

def run_settings(ui, ss, running):
    ui.fillScreenWithWhite()
    ui.flipDisplay()
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                return False
            elif (e.type == p.MOUSEBUTTONDOWN) \
                    & (p.mouse.get_pos()[0] < ui.WINDOW_WIDTH) & (p.mouse.get_pos()[1] < ui.WINDOW_HEIGHT):
                ui.checkBackButtonPressed()
                ui.evaluateSettingsChanges(ss)
                if ui.backButton:
                    ui.backButton = False
                    return True
        ui.drawSettingsState(ss)
        ui.tickClock()
        ui.flipDisplay()

def run_single_machine_multiplayer(ss, ui, running):
    #game screen
    mode = "oneMultiplayer"
    gs = GameState()
    gameClock = Clock(ss.clockLength, ss.clockIncrement, ss.clockLength, ss.clockIncrement)
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
    ui.flipDisplay()
    legalMoves = gs.getLegalMoves()
    #game loop
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif (e.type == p.MOUSEBUTTONDOWN) & (p.mouse.get_pos()[0] < ui.WIDTH) & (p.mouse.get_pos()[1] < ui.HEIGHT) & (not gameComplete):
                location = p.mouse.get_pos()
                column = int(location[0] / ui.SQ_SIZE)
                row = ui.adjustForFlipBoard(int(location[1] / ui.SQ_SIZE), gs.whiteToMove, ss.flipBoard, mode)
                if sqSelected == (row, column):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, column)
                    playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = Move(playerClicks[0], playerClicks[1], gs.board)
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
            ui.animateMove(gs, ss, mode)
            legalMoves = gs.getLegalMoves()
            moveMade = False
        if not gameComplete:
            if len(gs.moveLog) > 0:
                num_ticks = num_ticks + 1
                if(num_ticks >= ui.FPS):
                    gameClock.updateClock(gs.getTurnColor())
                    num_ticks = 0
                    if gameClock.whiteBaseTime == 0:
                        whiteTimeout = True
                    elif gameClock.blackBaseTime == 0:
                        blackTimeout = True
            ui.drawGameState(gs, ss, sqSelected, legalMoves, gameClock, whiteClockOn, mode)
            if gs.checkmate:
                gameComplete = True
                ui.drawEndOfGame("checkmate", color = gs.getOppColor(gs.getTurnColor()))
            elif gs.stalemate:
                gameComplete = True
                ui.drawEndOfGame("stalemate")
            elif tempInsufficientMaterial:
                gameComplete = True
                ui.drawEndOfGame("insufficientMaterial")
            elif tempRepetition:
                gameComplete = True
                ui.drawEndOfGame("repetition")
            elif tempFiftyMove:
                gameComplete = True
                ui.drawEndOfGame("fiftyMove")
            elif whiteTimeout:
                gameComplete = True
                ui.drawEndOfGame("whiteTimeout")
            elif blackTimeout:
                gameComplete = True
                ui.drawEndOfGame("blackTimeout")
        ui.tickClock()
        ui.flipDisplay()

def run_two_machine_multiplayer(ss, ui, running):
    #game screen
    mode = "twoMultiplayer"
    n = Network()
    gs = n.getGS()
    myColor = n.send("Requesting Color")

    #set mandatory default settings for this mode
    ss.undoMoveEnabled = False
    if myColor == "w":
        ss.flipBoard = False
    else:
        ss.flipBoard = True
    ss.clockLength = 10
    ss.clockIncrement = 10

    whiteClockOn = True
    gameComplete = False
    sqSelected = ()
    playerClicks = []
    moveMade = False
    generatedLegalMoves = False
    tempFiftyMove = False
    tempRepetition = False
    tempInsufficientMaterial = False
    whiteTimeout = False
    blackTimeout = False
    ui.flipDisplay()
    legalMoves = gs.getLegalMoves()
    #game loop
    while running:
        gameClock = n.send("Requesting Clock")
        timeout = n.send("Requesting Timeout")
        if timeout == "white timeout":
            whiteTimeout = True
        elif timeout == "black timeout":
            blackTimeout = True
        if myColor == gs.getTurnColor():
            #inside turn loop
            if not generatedLegalMoves:
                legalMoves = gs.getLegalMoves()
                generatedLegalMoves = True
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif (e.type == p.MOUSEBUTTONDOWN) & (p.mouse.get_pos()[0] < ui.WIDTH) & (p.mouse.get_pos()[1] < ui.HEIGHT) & (not gameComplete):
                    location = p.mouse.get_pos()
                    column = int(location[0] / ui.SQ_SIZE)
                    row = ui.adjustForFlipBoard(int(location[1] / ui.SQ_SIZE), gs.whiteToMove, ss.flipBoard, mode)
                    if sqSelected == (row, column):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, column)
                        playerClicks.append(sqSelected)
                        if len(playerClicks) == 2:
                            move = Move(playerClicks[0], playerClicks[1], gs.board)
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
                msg = n.send("Increment " + myColor)
                ui.animateMove(gs, ss, mode)
                generatedLegalMoves = False
                moveMade = False
                msg = n.send(gs)
        elif myColor != gs.getTurnColor():
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif (e.type == p.MOUSEBUTTONDOWN) & (p.mouse.get_pos()[0] < ui.WIDTH) & (p.mouse.get_pos()[1] < ui.HEIGHT) & (not gameComplete):
                    print("Not your turn")
            gs = n.send("Requesting GameState")
        if not gameComplete:
            ui.drawGameState(gs, ss, sqSelected, legalMoves, gameClock, whiteClockOn, mode)
            if gs.checkmate:
                gameComplete = True
                ui.drawEndOfGame("checkmate", color = gs.getOppColor(gs.getTurnColor()))
            elif gs.stalemate:
                gameComplete = True
                ui.drawEndOfGame("stalemate")
            elif tempInsufficientMaterial:
                gameComplete = True
                ui.drawEndOfGame("insufficientMaterial")
            elif tempRepetition:
                gameComplete = True
                ui.drawEndOfGame("repetition")
            elif tempFiftyMove:
                gameComplete = True
                ui.drawEndOfGame("fiftyMove")
            elif whiteTimeout:
                gameComplete = True
                ui.drawEndOfGame("whiteTimeout")
            elif blackTimeout:
                gameComplete = True
                ui.drawEndOfGame("blackTimeout")
        ui.tickClock()
        ui.flipDisplay()

main()