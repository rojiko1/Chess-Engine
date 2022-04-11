import pygame as p

class MenuState():

    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT):
        self.startButton = False
        self.settingsButton = False
        self.buttonWidth = WINDOW_WIDTH * (200 / 1280)
        self.buttonHeight = WINDOW_HEIGHT * (80 / 800)
        self.startButtonLocation = (((WINDOW_WIDTH - self.buttonWidth) / 2) - (WINDOW_WIDTH / 8), (WINDOW_HEIGHT - self.buttonHeight) / 1.4)
        self.settingsButtonLocation = (((WINDOW_WIDTH - self.buttonWidth) / 2) + (WINDOW_WIDTH / 8), (WINDOW_HEIGHT - self.buttonHeight) / 1.4)

    def checkStartButtonPressed(self):
        if (self.startButtonLocation[0] < p.mouse.get_pos()[0] < (self.startButtonLocation[0] + self.buttonWidth)) & (self.startButtonLocation[1] < p.mouse.get_pos()[1] < (self.startButtonLocation[1] + self.buttonHeight)):
            self.startButton = True

    def checkSettingsButtonPressed(self):
        if (self.settingsButtonLocation[0] < p.mouse.get_pos()[0] < (self.settingsButtonLocation[0] + self.buttonWidth)) & (self.settingsButtonLocation[1] < p.mouse.get_pos()[1] < (self.settingsButtonLocation[1] + self.buttonHeight)):
            self.settingsButton = True

class SettingsState():

    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT):
        self.backButton = False
        self.buttonWidth = WINDOW_WIDTH * (170 / 1280)
        self.buttonHeight = WINDOW_HEIGHT * (60 / 800)
        self.backButtonLocation = (WINDOW_WIDTH - self.buttonWidth, WINDOW_HEIGHT - self.buttonHeight)
        #self.flipBoardLocation = 1
        self.boardColorSchemeLocation = (0.2 * WINDOW_WIDTH, 0.32 * WINDOW_HEIGHT)
        self.moveHighlightingLocation = (0.2 * WINDOW_WIDTH, 0.57 * WINDOW_HEIGHT)
        self.autoQueenLocation = (0.2 * WINDOW_WIDTH, 0.82 * WINDOW_HEIGHT)
        self.pieceStyleLocation = ((0.8 * WINDOW_WIDTH) - (2 * self.buttonWidth), 0.32 * WINDOW_HEIGHT)
        self.undoMoveLocation = ((0.8 * WINDOW_WIDTH) - (2 * self.buttonWidth), 0.57 * WINDOW_HEIGHT)

        defaultSettings = open("defaultSettings.txt", "r")
        defaultSettingsLines = defaultSettings.readlines()
        defaultSettings.close()
        self.numSettings = 5
        self.clockLength = 10
        self.clockIncrement = 10
        self.flipBoard = False
        self.boardColorScheme = defaultSettingsLines[0][:-1]
        self.highlightValidMoves = eval(defaultSettingsLines[1])
        self.autoQueen = eval(defaultSettingsLines[2])
        self.pieceStyle = defaultSettingsLines[3][:-1]
        self.undoMoveEnabled = eval(defaultSettingsLines[4])

    def checkBackButtonPressed(self):
        if (self.backButtonLocation[0] < p.mouse.get_pos()[0] < (self.backButtonLocation[0] + self.buttonWidth)) & (self.backButtonLocation[1] < p.mouse.get_pos()[1] < (self.backButtonLocation[1] + self.buttonHeight)):
            self.backButton = True

    def evaluateSettingsChanges(self):
        x = p.mouse.get_pos()[0]
        y = p.mouse.get_pos()[1]
        if (x > self.boardColorSchemeLocation[0]) & (x < self.boardColorSchemeLocation[0] + (2 * self.buttonWidth)) & (y > self.boardColorSchemeLocation[1]) & (y < self.boardColorSchemeLocation[1] + self.buttonHeight):
            if x < (self.boardColorSchemeLocation[0] + self.buttonWidth):
                self.boardColorScheme = "coffee"
            else:
                self.boardColorScheme = "greyscale"
        if (x > self.moveHighlightingLocation[0]) & (x < self.moveHighlightingLocation[0] + (2 * self.buttonWidth)) & (y > self.moveHighlightingLocation[1]) & (y < self.moveHighlightingLocation[1] + self.buttonHeight):
            if x < (self.moveHighlightingLocation[0] + self.buttonWidth):
                self.highlightValidMoves = True
            else:
                self.highlightValidMoves = False
        if (x > self.autoQueenLocation[0]) & (x < self.autoQueenLocation[0] + (2 * self.buttonWidth)) & (y > self.autoQueenLocation[1]) & (y < self.autoQueenLocation[1] + self.buttonHeight):
            if x < (self.autoQueenLocation[0] + self.buttonWidth):
                self.autoQueen = True
            else:
                self.autoQueen = False
        if (x > self.pieceStyleLocation[0]) & (x < self.pieceStyleLocation[0] + (2 * self.buttonWidth)) & (y > self.pieceStyleLocation[1]) & (y < self.pieceStyleLocation[1] + self.buttonHeight):
            if x < (self.pieceStyleLocation[0] + self.buttonWidth):
                self.pieceStyle = "standard"
            else:
                self.pieceStyle = "leipzig"
        if (x > self.undoMoveLocation[0]) & (x < self.undoMoveLocation[0] + (2 * self.buttonWidth)) & (y > self.undoMoveLocation[1]) & (y < self.undoMoveLocation[1] + self.buttonHeight):
            if x < (self.undoMoveLocation[0] + self.buttonWidth):
                self.undoMoveEnabled = True
            else:
                self.undoMoveEnabled = False

class SpriteSheet():

    def __init__(self, image, rows, cols):
        self.spritesheet = image
        self.width = self.spritesheet.get_width()
        self.height = self.spritesheet.get_height()
        self.rows = rows
        self.cols = cols
        self.sqWidth = self.width / cols
        self.sqHeight = self.height / rows

    def getSubImageByIndex(self, row, col):
        subimage = self.spritesheet.subsurface(self.spritesheet.get_rect(topleft=(col * self.sqWidth, row * self.sqHeight), size=(self.sqWidth, self.sqHeight)))
        return subimage