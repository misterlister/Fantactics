import socket
from constants import *
from errors import *
import time
import random
from queue import Queue

this_file = "serverConnection.py"

class Player:

    def __init__(self, conn: socket, colour: str):
        self.conn = conn
        self.id = self.conn.fileno()
        self.colour = colour
        self. outbox = Queue()
    
    def getConn(self) -> socket:
        return self.conn
    
    def getID(self) -> socket:
        return self.id
    
    def getColour(self) -> socket:
        return self.colour
        
    def sendString(self, message: str) -> bool:
        if len(message) > MAX_MESSAGE_SIZE:
            errorMessage(this_file, "Message to server is too long.")
            return False

        else:
            self.outbox.put(message)
            while not self.outbox.empty():
                try:
                    packet = self.outbox.get().encode('ascii')
                except:
                    errorMessage(this_file, "Could not encode message into packet.")
                try:
                    self.conn.send(packet)
                
                except: 
                    errorMessage("Could not send message to ", self.colour, "player.")
                        
    
    def startTurn(self) -> bool:
        self.sendString("[Turn:YOU]")

    def stopTurn(self) -> bool:
        self.sendString("[Turn:OPP]")
    
    def initializeBoard(self):
        self.sendstring("[Board: INIT]")

def assignColours(p1Conn: socket, p2Conn: socket) -> tuple[Player,Player]:
    randomNumber = random.randint(1,100)
    
    if randomNumber%2 == 0:
        bluePlayer = Player(p1Conn, "blue")
        redPlayer = Player(p2Conn, "red")
    
    else:
        bluePlayer = Player(p2Conn, "blue")
        redPlayer = Player(p1Conn, "red")
    
    bluePlayer.sendString("[Clr:BLUE]")
    redPlayer.sendString("[Clr:RED]")

    return bluePlayer, redPlayer