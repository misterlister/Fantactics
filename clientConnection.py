import socket
from constants import *


serverIP = "localhost"
port = 5000
myTurn = False
playerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    
