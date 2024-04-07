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
        self.game = menu.game

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
            
        if message[1:4] == "MAP":
            mname = message[5:-1]
            self.game.set_map_name(mname)

        if message == "[CLR:BLACK]":
            self.game.set_player_colour("black")


        if message == "[RDY]":
            self.menu.setOpponentReady()
        
        if message == "[YOURTURN]":
            pass
            #self.menu.setOpponentReady()
            #self.state.next_turn()

        if(message[1:5]=="MOVE"):
            move_str = message[6:-1]
            params = move_str.split(",")
            action_space = self.game.board.get_space(int(params[1]),int(params[2]))
            target_space = self.game.board.get_space(int(params[5]),int(params[6]))
            unit_space = self.game.board.get_space(int(params[3]),int(params[4]))
            unit = unit_space.get_unit()
            self.game.board.chng_action_space(action_space)
            self.game.board.move_and_wait(unit,target_space)

        if(message[1:5]=="ATTK"):
            move_str = message[6:-1]
            params = move_str.split(",")
            print ("ATTACK PARAMS:")
            print(params)
            action_space = self.game.board.get_space(int(params[1]),int(params[2]))
            target_space = self.game.board.get_space(int(params[5]),int(params[6]))
            unit_space = self.game.board.get_space(int(params[3]),int(params[4]))
            unit = unit_space.get_unit()
            self.game.board.chng_action_space(action_space)
            self.game.board.attack_action(unit,target_space)
    
        if(message[1:5]=="ABIL"):
            move_str = message[6:-1]
            params = move_str.split(",")
            print ("ABILITY PARAMS:")
            print(params)
            action_space = self.game.board.get_space(int(params[1]),int(params[2]))
            target_space = self.game.board.get_space(int(params[5]),int(params[6]))
            unit_space = self.game.board.get_space(int(params[3]),int(params[4]))
            unit = unit_space.get_unit()
            self.game.board.chng_action_space(action_space)
            self.game.board.ability_action(unit,target_space)
        return True

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


