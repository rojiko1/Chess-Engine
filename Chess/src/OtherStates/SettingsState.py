class SettingsState():

    def __init__(self):
        defaultSettings = open("../defaultSettings.txt", "r")
        defaultSettingsLines = defaultSettings.readlines()
        defaultSettings.close()
        self.numSettings = 5
        self.clockLength = 10
        self.clockIncrement = 10
        self.boardColorScheme = defaultSettingsLines[0][:-1]
        self.highlightValidMoves = eval(defaultSettingsLines[1])
        self.autoQueen = eval(defaultSettingsLines[2])
        self.pieceStyle = defaultSettingsLines[3][:-1]
        self.undoMoveEnabled = eval(defaultSettingsLines[4])
        self.flipBoard = eval(defaultSettingsLines[5])