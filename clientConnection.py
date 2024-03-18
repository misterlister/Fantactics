import socket
from constants import *
import time
import threading
from tkinter import Tk
from globals import *
from errors import *

this_file = "clientConnection.py"

class receiver():

    def __init__(self, sock):
        
        self.socket = sock
        self.__thread = threading.Thread(target=self.__threadFunction, args=())
        self.__thread.daemon = True
        self.__thread.start()

    def __threadFunction(self) -> None:
        while not gameClosedEvent.is_set() or not connClosedEvent.is_set():
            
            try:
                serverPacket= self.socket.recv(MAX_MESSAGE_SIZE)
        
                if serverPacket:
                    parseMessage(serverPacket.decode('ascii'))

                else:
                    break
            
            except:
                print("No message received")

        setConnClosed()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
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

def parseMessage (message: str) -> bool:
    print("Server Message: ",message)
    
    if message == "[Turn:YOU]":
        setMyTurn()

    if message == "[Turn:OPP]":
        setOppTurn()

    return True

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

def setMyTurn():
    lock.acquire()
    myTurn.set()
    lock.release()

def setOppTurn():
    lock.acquire()
    myTurn.clear()
    lock.release()