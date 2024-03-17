import socket
from constants import *
import time
import threading
from tkinter import Tk
from globals import *
from clientConnection import *
from messageHandler import *

serverIP = "localhost"
port = 5000
playerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
playerSocket.settimeout(2)
def conn_thread():

    if not establishConnection():
        return
    
    while True:
        time.sleep(5)
        try:
            send("Ping")
            serverPacket= playerSocket.recv(MAX_MESSAGE_SIZE)
            if serverPacket:
                parseMessage(serverPacket.decode('ascii'))
        except:
            pass
        if gameClosedEvent.is_set():
            break

threadConn = threading.Thread(target=conn_thread)
threadConn.setDaemon = True

def establishConnection():
    try:
        playerSocket.connect((serverIP, port))
    except:
        print("Failed to connect to server.")
        return False
    print("Connection to server established")
    return True
    
def send(message):
    if len(message) > MAX_MESSAGE_SIZE:
        print("Message from client to server is too long")
    else:
        packet = message.encode("ascii")
        playerSocket.sendall(packet)

def checkConn():
    if threadConn.is_alive() and not connClosedEvent.is_set():
        root.after(1000, checkConn)
    else:
        print("Connection closed. Exiting Program")
        root.destroy()
