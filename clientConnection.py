from constants import *
import time
import threading
from tkinter import Tk
from errors import *
from queue import Queue
from gameState import Player
from clientSender import *
from gameBoard import *
from events import *

this_file = "clientConnection.py"

class Receiver():

    def __init__(self, sock, menu):
        
        self.sock = sock
        self.__thread = threading.Thread(target=self.__threadFunction, args=())
        self.__thread.daemon = True
        self.__thread.start()
        self.inbox = Queue()
        self.p1 = None
        self.p2 = None
        self.menu = menu
        self.game = self.menu.game

    def __threadFunction(self) -> None:
        
        while not (gameClosedEvent.is_set() or connClosedEvent.is_set()):

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
        print("RECEIVED::::", message)

        if message == "[CLR:WHITE]":
            self.game.set_player_colour("white")

        if message == "[CLR:BLACK]":
            self.game.set_player_colour("black")

        if message == "[RDY]":
            self.menu.setOpponentReady()
        
        if message == "[YOURTURN]":
            self.menu.setOpponentReady()
            self.state.next_turn()

        return True

    def setPlayerColours(self, playerColour: str, opponentColour: str):
                    
        print("Setting player to: ", playerColour)

        print("Player get_colour()", self.player.get_colour())

    def intializeBoards(self):
        self.gamestate.setup_board()
        self.opponent.setup_board()

    def killConnection(self):
        setConnClosed()

# End of receiver class.
    


def establishConn(ip, port) -> tuple[bool, socket.socket]:
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        sock.settimeout(TIMEOUT_LENGTH)

    except:
        errorMessage(this_file, "Could not establish connection.")
        setConnClosed()
        return False, None

    setConnOpen()
    print("Connected to server.")
    return True, sock


