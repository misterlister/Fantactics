import socket
from constants import *
from errors import errorMessage
import time
import random
from queue import Queue

this_file = "serverPlayer.py"

class Player:

    def __init__(self, conn: socket, colour: str):
        self.conn = conn
        self.id = self.conn.fileno()
        self.colour = colour
        self.outbox = Queue()
        self.__my_turn = None
    
    def getConn(self) -> socket:
        return self.conn
    
    def getID(self) -> socket:
        return self.id
    
    def getColour(self) -> socket:
        return self.colour
        
    def sendString(self, message: str) -> bool:
        
        message += ' '
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
                    return False
                try:
                    self.conn.send(packet)
                    time.sleep(.25)
                
                except: 
                    errorMessage("Could not send message to " + self.colour + "player.")
                    return False
            return True
                        
    
    def startTurn(self) -> bool:
        self.__my_turn = True
        return self.sendString("[Turn:YOU]")

    def stopTurn(self) -> bool:
        self.__my_turn = False
        return self.sendString("[Turn:OPP]")
    
    def isMyTurn(self) -> bool:
        return self.__my_turn
    
    def initializeBoard(self) -> bool:
        return self.sendString("[Board:INIT]")

def initializePlayers(p1_conn: socket, p2_conn: socket) -> tuple[Player,Player]:
    randomNumber = random.randint(1,100)
    
    if randomNumber%2 == 0:
        bluePlayer = Player(p1_conn, "blue")
        redPlayer = Player(p2_conn, "red")
    
    else:
        bluePlayer = Player(p2_conn, "blue")
        redPlayer = Player(p1_conn, "red")
    

    return bluePlayer, redPlayer