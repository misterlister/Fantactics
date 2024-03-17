import socket
from constants import *
import time
import threading
from tkinter import Tk
from globals import *
from clientConnection import *

serverIP = "localhost"
port = 5000
playerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def conn_thread():

    while True:
        time.sleep(0.25)
        print("Connection Thread Active")
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
    return True

def update(root):
    send("PING!")
    root.after(1000, lambda: update(root))   



def send(message):
    if len(message) > MAX_MESSAGE_SIZE:
        print("Message from client to server is too long")
    else:
        packet = message.encode("ascii")
        print("Message: ", message)
        print("Length of Message: ",len(message))
        print("Size of packet: ",len(packet))
        playerSocket.sendall(packet)

def checkConn():
    if threadConn.is_alive() and not connClosedEvent.is_set():
        root.after(1000, checkConn)
    else:
        print("Connection closed. Exiting Program")
        root.destroy()
