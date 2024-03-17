import socket
from constants import *
import time
import threading
from tkinter import Tk
from globals import *
from clientConnection import *
from messageHandler import *

class clientConnection():

    def __init__(self, ip: str, port, timeout:int = 2):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.socket.connect((ip, port))
            self.socket.settimeout(timeout)
        except:
            print("Could not connect!")
            self.setConnClosed()
            return

        self.setConnOpen()
        print("Connected to server.")

        self.__thread = threading.Thread(target=self.__threadFunction, args=())
        self.__thread.daemon = True
        self.__thread.start()

    def __del__(self):
        self.__thread.join()
        self.setConnClosed()
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
    
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

        self.__del__(self)
 
    def send(self, message:str) -> bool:
        print("SEND FN")
        if len(message) > MAX_MESSAGE_SIZE:
            print("Message from client to server is too long")
            return False
        
        else:
            packet = message.encode("ascii")

            try:
                self.socket.sendall(packet)
            
            except:
                print("\nCould not send msg to server.\n")
                self.setConnClosed()
                return False
    
    def joinThread(self) -> None:
        self.__thread.join()

    def setConnClosed(self):
        lock.acquire()
        connClosedEvent.set()
        lock.release()

    def setConnOpen(self):
        lock.acquire()
        connClosedEvent.clear()
        lock.release()