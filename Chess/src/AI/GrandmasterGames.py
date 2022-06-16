import chess.pgn
import time
import threading

from Chess.src.Engine.Move import Move

class GrandmasterGames():

    def __init__(self):
        self.anandGames = []
        self.carlsenGames = []
        self.dingGames = []
        self.firouzjaGames = []
        self.kasparovGames = []
        self.nakamuraGames = []

    def loadGames(self, choice):
        #if first letter of player's name is in choice, player's name will be loaded

        if "a" in choice:
            #load Anand games
            anand_thread = threading.Thread(target=self.loadAnandGames(), args=())
            anand_thread.daemon = True
            anand_thread.start()

        if "c" in choice:
            #load Carlsen games
            carlsen_thread = threading.Thread(target=self.loadCarlsenGames(), args=())
            carlsen_thread.daemon = True
            carlsen_thread.start()

        if "d" in choice:
            #load Ding games
            ding_thread = threading.Thread(target=self.loadDingGames(), args=())
            ding_thread.daemon = True
            ding_thread.start()

        if "f" in choice:
            #load Firouzja games
            firouzja_thread = threading.Thread(target=self.loadFirouzjaGames(), args=())
            firouzja_thread.daemon = True
            firouzja_thread.start()

        if "k" in choice:
            #load Kasparov games
            kasparov_thread = threading.Thread(target=self.loadKasparovGames(), args=())
            kasparov_thread.daemon = True
            kasparov_thread.start()

        if "n" in choice:
            #load Nakamura games
            nakamura_thread = threading.Thread(target=self.loadNakamuraGames(), args=())
            nakamura_thread.daemon = True
            nakamura_thread.start()

    def loadAnandGames(self):
        before = time.time()
        anandGamesPGN = open("../../assets/games/Anand.pgn", "r")
        for n in range(3965): #3965 games available
            self.anandGames.append(chess.pgn.read_game(anandGamesPGN))
        anandGamesPGN.close()
        end = time.time()
        print("Time Elapsed:", str(end - before), "s")

    def loadCarlsenGames(self):
        before = time.time()
        carlsenGamesPGN = open("../../assets/games/Carlsen.pgn", "r")
        for n in range(4089): #4089 games available
            self.carlsenGames.append(chess.pgn.read_game(carlsenGamesPGN))
        carlsenGamesPGN.close()
        end = time.time()
        print("Time Elapsed:", str(end - before), "s")

    def loadDingGames(self):
        before = time.time()
        dingGamesPGN = open("../../assets/games/Ding.pgn", "r")
        for n in range(1746): #1746 games available
            self.dingGames.append(chess.pgn.read_game(dingGamesPGN))
        dingGamesPGN.close()
        end = time.time()
        print("Time Elapsed:", str(end - before), "s")

    def loadFirouzjaGames(self):
        before = time.time()
        firouzjaGamesPGN = open("../../assets/games/Firouzja.pgn", "r")
        for n in range(1876): #1876 games available
            self.firouzjaGames.append(chess.pgn.read_game(firouzjaGamesPGN))
        firouzjaGamesPGN.close()
        end = time.time()
        print("Time Elapsed:", str(end - before), "s")

    def loadKasparovGames(self):
        before = time.time()
        kasparovGamesPGN = open("../../assets/games/Kasparov.pgn", "r")
        for n in range(2128): #2128 games available
            self.kasparovGames.append(chess.pgn.read_game(kasparovGamesPGN))
        kasparovGamesPGN.close()
        end = time.time()
        print("Time Elapsed:", str(end - before), "s")

    def loadNakamuraGames(self):
        before = time.time()
        nakamuraGamesPGN = open("../../assets/games/Nakamura.pgn", "r")
        for n in range(4811): #4811 games available
            self.nakamuraGames.append(chess.pgn.read_game(nakamuraGamesPGN))
        nakamuraGamesPGN.close()
        end = time.time()
        print("Time Elapsed:", str(end - before), "s")

    def notationToMove(self, notation, board):
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
        return number

gg = GrandmasterGames()
gg.loadGames("acdfkn")