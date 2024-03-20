from constants import *
import time
import threading
from tkinter import Tk
from globals import *
from errors import *
from queue import Queue
from gameState import Player
from clientSend import *

this_file = "clientConnection.py"

class receiver():

    def __init__(self, sock, player, opponent,gamestate):
        
        self.sock = sock
        self.__thread = threading.Thread(target=self.__threadFunction, args=())
        self.__thread.daemon = True
        self.__thread.start()
        self.inbox = Queue()
        self.player = player
        self.opponent = opponent
        self.gamestate = gamestate
        self.__connectionActive = True


    def __threadFunction(self) -> None:
        
        
        while not (gameClosedEvent.is_set() or connClosedEvent.is_set()):
            print("ConnClosedEvent: ", connClosedEvent.is_set())
            print("GameClosedEvent: ", connClosedEvent.is_set())

            try:
                serverPacket= self.sock.recv(MAX_MESSAGE_SIZE)
        
                if serverPacket:
                    str = serverPacket.decode('ascii')
                    msgs = str.split()
                    for msg in msgs:       
                        self.parseMessage(msg)
                else:
                    break
            
            except:
                # No message received this time.
                pass


    
    def parseMessage (self, message: str) -> bool:
    
        print(message)
        if message == "[Clr:BLUE]":
            print("Player is BLUE@#$!$")
            self.player.set_colour("blue")
            self.opponent.set_colour("red")
            print("PLAYER IS NOW: ", self.player.get_colour())

        if message == "[Clr:RED]":
            print("Player is RED@#$!$")
            self.player.set_colour("red")
            self.opponent.set_colour("blue")
            print("PLAYER IS NOW: ", self.player.get_colour())

        if message == "[Turn:YOU]":
            self.player.start_turn()

        if message == "[Turn:OPP]":
            self.opponent.start_turn()

        if message == "[Board:INIT]":
            self.intializeBoards()

        return True

    def setPlayerColours(self, playerColour: str, opponentColour: str):
                    
        print(" ffffffffffffffffffff Setting player to: ", playerColour)

        print("Player get_colour()", self.player.get_colour())

    def intializeBoards(self):
        self.gamestate.setup_board()
        self.opponent.setup_board()

    def killConnection(self):
        setConnClosed()

# End of receiver class.
    


def establishConn(ip, port, timeout) -> tuple[bool, socket.socket]:
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        sock.settimeout(timeout)

    except:
        errorMessage(this_file, "Could not establish connection.")
        setConnClosed()
        return False, None

    setConnOpen()
    print("Connected to server.")
    return True, sock


