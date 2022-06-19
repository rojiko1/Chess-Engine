import chess.pgn
import time
import threading

from Chess.src.Engine.Move import Move

class GrandmasterGames():

    def __init__(self):
        #number of games available for each player
        self.ANAND_NUM_GAMES = 3965
        self.CARLSEN_NUM_GAMES = 4089
        self.DING_NUM_GAMES = 1746
        self.FIROUZJA_NUM_GAMES = 1876
        self.KASPAROV_NUM_GAMES = 2128
        self.NAKAMURA_NUM_GAMES = 4811

        self.anandGames = []
        self.carlsenGames = []
        self.dingGames = []
        self.firouzjaGames = []
        self.kasparovGames = []
        self.nakamuraGames = []

        self.allGames = []

        self.matchingGames = []

    def loadAllGames(self):
        thread = threading.Thread(target=self.loadAllGames2, args=())
        thread.daemon = True
        thread.start()

    def loadAllGames2(self):
        #if first letter of player's name is in choice, player's name will be loaded

        #load Anand games
        anand_thread = threading.Thread(target=self.loadAnandGames, args=())
        anand_thread.daemon = True
        anand_thread.start()

        #load Carlsen games
        carlsen_thread = threading.Thread(target=self.loadCarlsenGames, args=())
        carlsen_thread.daemon = True
        carlsen_thread.start()

        #load Ding games
        ding_thread = threading.Thread(target=self.loadDingGames, args=())
        ding_thread.daemon = True
        ding_thread.start()

        #load Firouzja games
        firouzja_thread = threading.Thread(target=self.loadFirouzjaGames, args=())
        firouzja_thread.daemon = True
        firouzja_thread.start()

        #load Kasparov games
        kasparov_thread = threading.Thread(target=self.loadKasparovGames, args=())
        kasparov_thread.daemon = True
        kasparov_thread.start()

        #load Nakamura games
        self.loadNakamuraGames()

        #combine all players' games
        self.combineGames()

    def loadAnandGames(self):
        before = time.time()
        self.anandGames = []
        anandGamesPGN = open("../assets/games/Anand.pgn", "r")
        for n in range(self.ANAND_NUM_GAMES):
            self.anandGames.append(chess.pgn.read_game(anandGamesPGN))
        anandGamesPGN.close()
        end = time.time()
        print("Anand Time Elapsed:", str(end - before), "s")

    def loadCarlsenGames(self):
        before = time.time()
        self.carlsenGames = []
        carlsenGamesPGN = open("../assets/games/Carlsen.pgn", "r")
        for n in range(self.CARLSEN_NUM_GAMES):
            self.carlsenGames.append(chess.pgn.read_game(carlsenGamesPGN))
        carlsenGamesPGN.close()
        end = time.time()
        print("Carlsen Time Elapsed:", str(end - before), "s")

    def loadDingGames(self):
        before = time.time()
        self.dingGames = []
        dingGamesPGN = open("../assets/games/Ding.pgn", "r")
        for n in range(self.DING_NUM_GAMES):
            self.dingGames.append(chess.pgn.read_game(dingGamesPGN))
        dingGamesPGN.close()
        end = time.time()
        print("Ding Time Elapsed:", str(end - before), "s")

    def loadFirouzjaGames(self):
        before = time.time()
        self.firouzjaGames = []
        firouzjaGamesPGN = open("../assets/games/Firouzja.pgn", "r")
        for n in range(self.FIROUZJA_NUM_GAMES):
            self.firouzjaGames.append(chess.pgn.read_game(firouzjaGamesPGN))
        firouzjaGamesPGN.close()
        end = time.time()
        print("Firouzja Time Elapsed:", str(end - before), "s")

    def loadKasparovGames(self):
        before = time.time()
        self.kasparovGames = []
        kasparovGamesPGN = open("../assets/games/Kasparov.pgn", "r")
        for n in range(self.KASPAROV_NUM_GAMES):
            self.kasparovGames.append(chess.pgn.read_game(kasparovGamesPGN))
        kasparovGamesPGN.close()
        end = time.time()
        print("Kasparov Time Elapsed:", str(end - before), "s")

    def loadNakamuraGames(self):
        before = time.time()
        self.nakamuraGames = []
        nakamuraGamesPGN = open("../assets/games/Nakamura.pgn", "r")
        for n in range(self.NAKAMURA_NUM_GAMES):
            self.nakamuraGames.append(chess.pgn.read_game(nakamuraGamesPGN))
        nakamuraGamesPGN.close()
        finished = True
        end = time.time()
        print("Nakamura Time Elapsed:", str(end - before), "s")
        return finished

    def combineGames(self):
        before = time.time()
        self.allGames = []
        for index in range(self.NAKAMURA_NUM_GAMES): #Nakamura - most games
            self.allGames.append(self.nakamuraGames[index])
            if index < self.CARLSEN_NUM_GAMES:
                self.allGames.append(self.carlsenGames[index])
                if index < self.ANAND_NUM_GAMES:
                    self.allGames.append(self.anandGames[index])
                    if index < self.KASPAROV_NUM_GAMES:
                        self.allGames.append(self.kasparovGames[index])
                        if index < self.FIROUZJA_NUM_GAMES:
                            self.allGames.append(self.firouzjaGames[index])
                            if index < self.DING_NUM_GAMES:
                                self.allGames.append(self.dingGames[index])
        assert len(self.allGames) == (self.ANAND_NUM_GAMES + self.CARLSEN_NUM_GAMES + self.DING_NUM_GAMES + self.FIROUZJA_NUM_GAMES + self.KASPAROV_NUM_GAMES + self.NAKAMURA_NUM_GAMES)
        end = time.time()
        print("Time Elapsed:", str(end - before), "s")
        print("Len:", str(len(self.allGames)))

    def findMatchingGames(self, firstMove):
        pass

    def searchMatchingGames(self, playerArray):
        pass

    def narrowMatchingGames(self):
        pass

    '''def notationToMove(self, notation, board):
        startR = 8 - int(notation[1])
        startC = self.letterToNumber(notation[0])
        endR = 8 - int(notation[3])
        endC = self.letterToNumber(notation[2])
        move = Move((startR, startC), (endR, endC), board)
        if (move.pieceMoved[1] == "K") & (abs(endC - startC) == 2):
            move.castling = True
        elif ((move.pieceMoved[1] == "p") & (move.pieceCaptured == "--")) & (abs(endC - startC) == 1):
            move.enPassant = True
        return move

    def letterToNumber(self, letter):
        if letter == "a":
            number = 0
        elif letter == "b":
            number = 1
        elif letter == "c":
            number = 2
        elif letter == "d":
            number = 3
        elif letter == "e":
            number = 4
        elif letter == "f":
            number = 5
        elif letter == "g":
            number = 6
        elif letter == "h":
            number = 7
        return number'''

gg = GrandmasterGames()
gg.loadAllGames()
time.sleep(600.0)