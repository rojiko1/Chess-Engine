import pygame as p
import socket
from _thread import *
import pickle
import random
from Chess.src.Engine.GameState import GameState
from Chess.src.Engine.Clock import Clock

class Server():

    def __init__(self):
        server = "192.168.50.74"
        port = 5555

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((server, port))
        except socket.error as e:
            str(e)

        s.listen(2)
        print("Server started, waiting for connection")

        p.init()
        clock = p.time.Clock()

        self.defaultBaseTime = 10
        self.defaultIncrementTime = 10

        self.gameState = GameState()
        self.colors = ["w", "b"]
        self.gameClock = Clock(self.defaultBaseTime, self.defaultIncrementTime, self.defaultBaseTime, self.defaultIncrementTime)
        self.whiteClockOn = True
        self.num_ticks = 0
        self.whiteTimeout = False
        self.blackTimeout = False
        self.gameComplete = False
        self.checkmate = False
        self.stalemate = False
        self.resetGame = False
        self.wRequestReset = False
        self.bRequestReset = False

        whiteTaken = False
        blackTaken = False
        while True:
            clock.tick(30)
            if len(self.gameState.moveLog) > 0:
                self.num_ticks = self.num_ticks + 1
                if(self.num_ticks == 30):
                    self.gameClock.updateClock(self.gameState.getTurnColor())
                    self.num_ticks = 0
                    if self.gameClock.whiteBaseTime == 0:
                        self.whiteTimeout = True
                        self.gameComplete = True
                    elif self.gameClock.blackBaseTime == 0:
                        self.blackTimeout = True
                        self.gameComplete = True
            if self.wRequestReset & self.bRequestReset:
                self.resetGame = True
                self.gameState = GameState()
                self.colors = ["w", "b"]
                self.gameClock = Clock(self.defaultBaseTime, self.defaultIncrementTime, self.defaultBaseTime, self.defaultIncrementTime)
                self.whiteClockOn = True
                self.num_ticks = 0
                self.whiteTimeout = False
                self.blackTimeout = False
                self.gameComplete = False
                self.checkmate = False
                self.stalemate = False
            if (not whiteTaken) | (not blackTaken):
                conn, addr = s.accept()
                print("Connected to: ", addr)
                if (not whiteTaken) & (not blackTaken):
                    if random.random() < 0.5:
                        whiteTaken = True
                        start_new_thread(self.threaded_client, (conn, 0))
                    else:
                        blackTaken = True
                        start_new_thread(self.threaded_client, (conn, 1))
                elif whiteTaken:
                    blackTaken = True
                    start_new_thread(self.threaded_client, (conn, 1))
                elif blackTaken:
                    whiteTaken = True
                    start_new_thread(self.threaded_client, (conn, 0))

    def threaded_client(self, conn, currentPlayer):
        conn.send(pickle.dumps(self.gameState))
        reply = ""
        while True:
            try:
                data = pickle.loads(conn.recv(16384))
                if isinstance(data, GameState):
                    self.gameState = data
                    reply = "Received data"
                elif data == "Requesting GameState":
                    reply = self.gameState
                elif data == "Requesting Color":
                    reply = self.colors[currentPlayer]
                elif data == "Requesting Clock":
                    reply = self.gameClock
                elif data == "Increment w":
                    self.gameClock.increment("w")
                    reply = "incremented white"
                elif data == "Increment b":
                    self.gameClock.increment("b")
                    reply = "incremented black"
                elif data == "Requesting Timeout":
                    if self.whiteTimeout:
                        reply = "white timeout"
                    elif self.blackTimeout:
                        reply = "black timeout"
                elif data == "w Requesting Reset Game":
                    self.wRequestReset = True
                    reply = "Request Recieved"
                elif data == "b Requesting Reset Game":
                    self.bRequestReset = True
                    reply = "Request Recieved"
                elif data[2:] == "Requesting Reset Game Status":
                    reply = self.resetGame
                    if self.resetGame:
                        if data[0] == "w":
                            self.wRequestReset = False
                        elif data[0] == "b":
                            self.bRequestReset = False
                        if (not self.wRequestReset) & (not self.bRequestReset):
                            self.resetGame = False
                if not data:
                    print("Disconnected")
                    break
                else:
                    conn.sendall(pickle.dumps(reply))
            except:
                break

        print("Lost connection")
        conn.close()

server = Server()