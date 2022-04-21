import pygame as p
from playsound import playsound
import random

from Chess.src.Engine.Clock import Clock
from Chess.src.Engine.GameState import GameState
from Chess.src.Engine.Move import Move
from Chess.src.OtherStates.SettingsState import SettingsState
from Chess.src.UserInterface.UserInterface import UserInterface
from Chess.src.Server.Network import Network
from Chess.src.AI.Computer import Computer

#Project status: drag pieces to make move, scaling multiplayer w/ server, lichess api for AI, chess notation
#Current issue: start server from multiplayer, premove, game management when players disconnect, pawn move index out of range bug

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
        run_single_player(ss, ui, running)

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
    gameClock = Clock(ss.clockLength, ss.clockIncrement)
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
    whiteLTNotSounded = True
    blackLTNotSounded = True
    ui.flipDisplay()
    legalMoves = gs.getLegalMoves()
    #game loop
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif (e.type == p.MOUSEBUTTONDOWN) & (p.mouse.get_pos()[0] < ui.WIDTH) & (p.mouse.get_pos()[1] < ui.HEIGHT) & (not gameComplete):
                location = p.mouse.get_pos()
                column = ui.adjustForFlipBoard(int(location[0] / ui.SQ_SIZE), gs.whiteToMove, ss.flipBoard, mode)
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
                    whiteLTNotSounded = True
                    blackLTNotSounded = True
                    legalMoves = gs.getLegalMoves()
        if moveMade:
            gameClock.increment(gs.getOppColor(gs.getTurnColor()))
            whiteClockOn = not whiteClockOn
            num_ticks = 0
            ui.animateMove(gs, ss, mode)
            legalMoves = gs.getLegalMoves()
            moveMade = False
        if not gameComplete:
            if len(gs.moveLog) > 0: #handling game clock
                num_ticks = num_ticks + 1
                if(num_ticks >= ui.FPS):
                    gameClock.updateClock(gs.getTurnColor())
                    num_ticks = 0
                    if gameClock.whiteBaseTime == 0:
                        whiteTimeout = True
                    elif gameClock.blackBaseTime == 0:
                        blackTimeout = True
                    elif (gameClock.whiteBaseTime == (gameClock.lowTimeThreshold - 1)) | (gameClock.blackBaseTime == (gameClock.lowTimeThreshold - 1)):
                        playsound("../../assets/sounds/low_time_sound.mp3")
            ui.drawGameState(gs, ss, sqSelected, legalMoves, gameClock, whiteClockOn, mode)
            if gs.checkmate:
                gameComplete = True
                ui.drawEndOfGame("checkmate", color = gs.getOppColor(gs.getTurnColor()))
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif gs.stalemate:
                gameComplete = True
                ui.drawEndOfGame("stalemate")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif tempInsufficientMaterial:
                gameComplete = True
                ui.drawEndOfGame("insufficientMaterial")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif tempRepetition:
                gameComplete = True
                ui.drawEndOfGame("repetition")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif tempFiftyMove:
                gameComplete = True
                ui.drawEndOfGame("fiftyMove")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif whiteTimeout:
                gameComplete = True
                ui.drawEndOfGame("whiteTimeout")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif blackTimeout:
                gameComplete = True
                ui.drawEndOfGame("blackTimeout")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
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
    whiteLTNotSounded = True
    blackLTNotSounded = True
    ui.flipDisplay()
    legalMoves = gs.getLegalMoves()
    #game loop
    while running:
        if not gameComplete:
            gameClock = n.send("Requesting Clock")
            if gameClock.whiteBaseTime == 0:
                whiteTimeout = True
            elif gameClock.blackBaseTime == 0:
                blackTimeout = True
            elif ((myColor == "w") & (gameClock.whiteBaseTime == gameClock.lowTimeThreshold)) & whiteLTNotSounded:
                playsound("../../assets/sounds/low_time_sound.mp3")
                whiteLTNotSounded = False
            elif ((myColor == "b") & (gameClock.blackBaseTime == gameClock.lowTimeThreshold)) & blackLTNotSounded:
                playsound("../../assets/sounds/low_time_sound.mp3")
                blackLTNotSounded = False
            if myColor == gs.getTurnColor():
                #inside turn loop
                if not generatedLegalMoves:
                    if ((myColor == "w") & (not whiteClockOn)) | ((myColor == "b") & (whiteClockOn)):
                        whiteClockOn = not whiteClockOn
                    legalMoves = gs.getLegalMoves()
                    generatedLegalMoves = True
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    elif (e.type == p.MOUSEBUTTONDOWN) & (p.mouse.get_pos()[0] < ui.WIDTH) & (p.mouse.get_pos()[1] < ui.HEIGHT) & (not gameComplete):
                        location = p.mouse.get_pos()
                        column = ui.adjustForFlipBoard(int(location[0] / ui.SQ_SIZE), gs.whiteToMove, ss.flipBoard,
                                                       mode)
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
                if moveMade:
                    msg = n.send("Increment " + myColor)
                    ui.animateMove(gs, ss, mode)
                    generatedLegalMoves = False
                    moveMade = False
                    whiteClockOn = not whiteClockOn
                    gs.getLegalMoves()
                    msg = n.send(gs)
            elif myColor != gs.getTurnColor():
                for e in p.event.get():
                    if e.type == p.QUIT:
                        running = False
                    elif (e.type == p.MOUSEBUTTONDOWN) & (p.mouse.get_pos()[0] < ui.WIDTH) & (p.mouse.get_pos()[1] < ui.HEIGHT) & (not gameComplete):
                        print("Not your turn")
                gs = n.send("Requesting GameState")

            ui.drawGameState(gs, ss, sqSelected, legalMoves, gameClock, whiteClockOn, mode)
            if gs.checkmate | gs.stalemate:
                ui.drawGameState(gs, ss, sqSelected, legalMoves, gameClock, not gs.whiteToMove, mode)
            if gs.checkmate:
                gameComplete = True
                ui.drawEndOfGame("checkmate", color = gs.getOppColor(gs.getTurnColor()))
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif gs.stalemate:
                gameComplete = True
                ui.drawEndOfGame("stalemate")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif tempInsufficientMaterial:
                gameComplete = True
                ui.drawEndOfGame("insufficientMaterial")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif tempRepetition:
                gameComplete = True
                ui.drawEndOfGame("repetition")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif tempFiftyMove:
                gameComplete = True
                ui.drawEndOfGame("fiftyMove")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif whiteTimeout:
                gameComplete = True
                ui.drawEndOfGame("whiteTimeout")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif blackTimeout:
                gameComplete = True
                ui.drawEndOfGame("blackTimeout")
                playsound("../../assets/sounds/end_of_game_sound.mp3")

        if gameComplete:
            resetGame = n.send(myColor + " Requesting Reset Game Status")
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif (e.type == p.KEYDOWN):
                    if e.key == p.K_x: #reset gameState
                        msg = n.send(myColor + " Requesting Reset Game")
                        print("Game Reset Request Sent.")
            if resetGame:
                gs = n.send("Requesting GameState")
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
                whiteLTNotSounded = True
                blackLTNotSounded = True

        ui.tickClock()
        ui.flipDisplay()

def run_single_player(ss, ui, running):
    #game screen
    mode = "singlePlayer"

    if random.random() < 0.5:
        myColorIsWhite = True
        myColor = "w"
        compColor = "b"
        ss.flipBoard = False
    else:
        myColorIsWhite = False
        myColor = "b"
        compColor = "w"
        ss.flipBoard = True

    gs = GameState()
    computer = Computer(compColor)
    gameClock = Clock(ss.clockLength, ss.clockIncrement)
    whiteClockOn = True
    num_ticks = 0
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
    LTNotSounded = True
    sentComputerMoveRequest = False
    ui.flipDisplay()
    legalMoves = gs.getLegalMoves()
    #game loop
    while running:
        if myColorIsWhite == gs.whiteToMove:
            if not generatedLegalMoves:
                if ((myColor == "w") & (not whiteClockOn)) | ((myColor == "b") & (whiteClockOn)):
                    whiteClockOn = not whiteClockOn
                legalMoves = gs.getLegalMoves()
                generatedLegalMoves = True
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif (e.type == p.MOUSEBUTTONDOWN) & (p.mouse.get_pos()[0] < ui.WIDTH) & (p.mouse.get_pos()[1] < ui.HEIGHT) & (not gameComplete):
                    location = p.mouse.get_pos()
                    column = ui.adjustForFlipBoard(int(location[0] / ui.SQ_SIZE), gs.whiteToMove, ss.flipBoard, mode)
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
                        LTNotSounded = True
                        legalMoves = gs.getLegalMoves()
            if moveMade:
                gameClock.increment(gs.getOppColor(gs.getTurnColor()))
                whiteClockOn = not whiteClockOn
                num_ticks = 0
                ui.animateMove(gs, ss, mode)
                legalMoves = gs.getLegalMoves()
                moveMade = False
                generatedLegalMoves = False
                sentComputerMoveRequest = False
        elif myColorIsWhite != gs.whiteToMove:
            if not sentComputerMoveRequest:
                length = len(gs.moveLog)
                computer.findOptimalMove(gs, gameClock, mode)
                sentComputerMoveRequest = True
            for e in p.event.get():
                if e.type == p.QUIT:
                    running = False
                elif (e.type == p.MOUSEBUTTONDOWN) & (p.mouse.get_pos()[0] < ui.WIDTH) & (p.mouse.get_pos()[1] < ui.HEIGHT) & (not gameComplete):
                    print("Not your turn")
            if len(gs.moveLog) == (length + 1):
                move = gs.moveLog[-1]
                gs.moveLog.pop(-1)
                gs.makeMove(move)
                ui.animateMove(gs, ss, mode)
                gameClock.increment(compColor)
                evaluation = computer.evaluator.evaluatePosition(gs.board)
        if not gameComplete:
            if len(gs.moveLog) > 0: #handling game clock
                num_ticks = num_ticks + 1
                if(num_ticks >= ui.FPS):
                    gameClock.updateClock(gs.getTurnColor())
                    num_ticks = 0
                    if gameClock.whiteBaseTime == 0:
                        whiteTimeout = True
                    elif gameClock.blackBaseTime == 0:
                        blackTimeout = True
                    elif ((myColorIsWhite & (gameClock.whiteBaseTime == gameClock.lowTimeThreshold)) | ((not myColorIsWhite) & (gameClock.blackBaseTime == gameClock.lowTimeThreshold))) & LTNotSounded:
                        playsound("../../assets/sounds/low_time_sound.mp3")
                        LTNotSounded = False
            ui.drawGameState(gs, ss, sqSelected, legalMoves, gameClock, whiteClockOn, mode)
            if gs.checkmate:
                gameComplete = True
                ui.drawEndOfGame("checkmate", color = gs.getOppColor(gs.getTurnColor()))
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif gs.stalemate:
                gameComplete = True
                ui.drawEndOfGame("stalemate")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif tempInsufficientMaterial:
                gameComplete = True
                ui.drawEndOfGame("insufficientMaterial")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif tempRepetition:
                gameComplete = True
                ui.drawEndOfGame("repetition")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif tempFiftyMove:
                gameComplete = True
                ui.drawEndOfGame("fiftyMove")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif whiteTimeout:
                gameComplete = True
                ui.drawEndOfGame("whiteTimeout")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
            elif blackTimeout:
                gameComplete = True
                ui.drawEndOfGame("blackTimeout")
                playsound("../../assets/sounds/end_of_game_sound.mp3")
        ui.tickClock()
        ui.flipDisplay()

main()