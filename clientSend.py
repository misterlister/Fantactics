from errors import errorMessage
from constants import *
from globals import *
import socket

this_file = "clientSend.py"

class Sender:

    sock = None

    def __init__(self,sock:socket):
        self.sock = sock

    def send(self, message:str) -> bool:
        
        if len(message) > MAX_MESSAGE_SIZE:
            errorMessage(this_file, "Message to server is too long.")
            return False
        
        else:
            message = message + '\n'
            packet = message.encode("ascii")

            try:
                self.sock.sendall(packet)
            
            except:
                errorMessage(this_file, "Could not send msg to server.")
                setConnClosed()
                return False
            
    def endfGame(self,event,root):
        self.sender("[Game:END]")
        gameClosedEvent.set()
        root.destroy()

        
def setConnClosed():
    connClosedEvent.set()

def setConnOpen():
    connClosedEvent.clear()

def setGameClosed():
    gameClosedEvent.set()

def setGameOpen():
    gameClosedEvent.clear()

