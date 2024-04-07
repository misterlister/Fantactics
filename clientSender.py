from errors import errorMessage
from constants import *
import socket
from events import *

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
            
    def kill(self,row, col):
        msg = "[Kill:" + str(row) + "," + str(col) +"]"
        self.send(msg)
    
    def move(self,prev_row, prev_col,new_row,new_col):
        prev_row = str(prev_row)
        prev_col = str(prev_col)
        new_row = str(new_row)
        new_col = str(new_col)
        msg = "[Move:" + prev_row + "," + prev_col + ":" 
        msg += new_row + "," + new_col + "]"
        self.send(msg)

    def change_hp(self,row,col,hp):
        msg = "[Hp:" + str(row) + "," + str(col) + ":"
        msg += str(hp) + "]" 
        self.send(msg)


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

