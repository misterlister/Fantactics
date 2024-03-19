import socket
from constants import *
import time
import threading
from tkinter import Tk
from globals import *
from errors import *
from queue import Queue
from gameState import Player

this_file = "clientConnection.py"

class receiver():

    def __init__(self, sock, player, opponent,gamestate):
        
        self.socket = sock
        self.__thread = threading.Thread(target=self.__threadFunction, args=())
        self.__thread.daemon = True
        self.__thread.start()
        self.inbox = Queue()
        self.player = player
        self.opponent = opponent
        self.gamestate = gamestate


    def __threadFunction(self) -> None:
        while not gameClosedEvent.is_set() or not connClosedEvent.is_set():
            
            try:
                serverPacket= self.socket.recv(MAX_MESSAGE_SIZE)
        
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

        setConnClosed()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
    
    def parseMessage (self, message: str) -> bool:
    
        print(message)
        if message == "[Clr:BLUE]":
            print("Player is BLUE@#$!$")
            lock.acquire()
            self.player.set_colour("blue")
            self.opponent.set_colour("red")
            lock.release()
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
        lock.acquire()
        self.gamestate.setup_board()
        self.opponent.setup_board()
        lock.release()


# End of receiver class.
        
def send(self, message:str) -> bool:
    
    if len(message) > MAX_MESSAGE_SIZE:
        errorMessage(this_file, "Message to server is too long.")
        return False
    
    else:
        packet = message.encode("ascii")

        try:
            self.socket.sendall(packet)
        
        except:
            errorMessage(this_file, "Could not send msg to server.")
            setConnClosed()
            return False



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

def setConnClosed():
    lock.acquire()
    connClosedEvent.set()
    lock.release()

def setConnOpen():
    lock.acquire()
    connClosedEvent.clear()
    lock.release()

