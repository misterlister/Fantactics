import socket
from constants import *
from errors import *
import time

this_file = "serverConnection.py"

class Player:

    def __init__(self, conn: socket, colour: str):
        self.conn = conn
        self.id = self.conn.fileno()
        self.colour = colour
    
    def getConn(self) -> socket:
        return self.conn
    
    def getID(self) -> socket:
        return self.id
    
    def getColour(self) -> socket:
        return self.colour
    
# End of Player Class
    
def sendString(conn: socket, message: str) -> bool:
    if len(message) > MAX_MESSAGE_SIZE:
        errorMessage(this_file, "Message to server is too long.")
        return False

    else:
        packet = message.encode("ascii")

        try:
            conn.sendall(packet)
        
        except:
            errorMessage(this_file, "Could not send msg to server.")
            return False
        
def setTurn(turnColour: str, blueConn, redConn) -> None:
    
    if turnColour == "blue":
        sendString(redConn, "[Turn:OPP]")
        sendString(blueConn, "[Turn:YOU]")

    elif turnColour == "red":
        sendString(blueConn, "[Turn:OPP]")
        sendString(redConn, "[Turn:YOU]")

    else: 
        errorMessage(this_file, "Bad turn colour.")
