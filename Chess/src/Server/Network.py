import socket
import pickle

class Network():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.50.74"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.gs = self.connect()

    def getGS(self):
        return self.gs

    def connect(self):
        try:
            self.client.connect(self.addr)
            #print(pickle.loads(self.client.recv(2048)))
            return pickle.loads(self.client.recv(16384))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(16384))
        except socket.error as e:
            print(e)