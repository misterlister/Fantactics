from errors import errorMessage
from constants import MAX_MESSAGE_SIZE
import socket
from events import (
    connClosedEvent,
    gameClosedEvent
)
from units import Unit
from space import Space

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

    def end_turn(self):
        self.send("[ENDTURN]")

    def move(self, action_space: Space, unit: Unit, target_space: Space):
        message = "[MOVE:"
        message += unit.get_unit_type() + ','
        message += str(action_space.get_row()) + ','
        message += str(action_space.get_col()) + ','
        message += str(unit.get_space().get_row()) + ','
        message += str(unit.get_space().get_col()) + ','
        message += str(target_space.get_row()) + ','
        message += str(target_space.get_col()) + ']'

        #print("Sending Move:")
        #print(message)
        self.send(message)



    def attack(self, action_space: Space, unit: Unit, target_space: Space):
        message = "[ATTK:"
        message += unit.get_unit_type() + ','
        message += str(action_space.get_row()) + ','
        message += str(action_space.get_col()) + ','
        message += str(unit.get_space().get_row()) + ','
        message += str(unit.get_space().get_col()) + ','
        message += str(target_space.get_row()) + ','
        message += str(target_space.get_col()) + ']'

        self.send(message)


    def ability(self, action_space, unit, target_space):
        
        message = "[ABIL:"
        message += unit.get_unit_type() + ','
        message += str(action_space.get_row()) + ','
        message += str(action_space.get_col()) + ','
        message += str(unit.get_space().get_row()) + ','
        message += str(unit.get_space().get_col()) + ','
        message += str(target_space.get_row()) + ','
        message += str(target_space.get_col()) + ']'
        self.send(message)



    def exit(self, root):
        self.send("[END]")
        print("Closing game.")
        root.destroy()
        gameClosedEvent.set()

        
def setConnClosed():
    connClosedEvent.set()

def setConnOpen():
    connClosedEvent.clear()

def setGameClosed():
    gameClosedEvent.set()

def setGameOpen():
    gameClosedEvent.clear()

