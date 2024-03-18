import socket
import selectors
from constants import *
import random
from serverConnection import *

IP = 'localhost'
PORT = 5000  
p1Active = False
p2Active = False
sel = selectors.DefaultSelector()

def receive(conn, mask):
    data = conn.recv(MAX_MESSAGE_SIZE)

    if data:
        if conn.fileno() == p1ID:
            print("Message from Player 1:")
        if conn.fileno() == p2ID:
            print("Message from Player 2:")
        print(data.decode('ascii'))
        conn.send(data)

    else:
        sel.unregister(conn)
        conn.close()

def assignPlayers() -> tuple[Player,Player]:
    randomNumber = random.randint(1,100)
    
    if randomNumber%2 == 0:
        bluePlayer = Player(p1Conn, "blue")
        redPlayer = Player(p2Conn, "red")
    
    else:
        bluePlayer = Player(p2Conn, "blue")
        redPlayer = Player(p1Conn, "red")
    
    return bluePlayer, redPlayer

if __name__ == "__main__":

    listenSocket = socket.socket()
    listenSocket.bind((IP,PORT))
    listenSocket.listen()

    print("Server listenining at hostname: ", IP, ", port: ", PORT)    
    p1Conn, p1Addr = listenSocket.accept()
    print("P1Conn type: ", type(p1Conn))
    p1ID = p1Conn.fileno()
    sel.register(p1Conn, selectors.EVENT_READ, receive)
    p1Active = True

    print("Welcome to Fantactics. Please wait for your opponent")
    p2Conn, p2Addr = listenSocket.accept()
    p2ID = p2Conn.fileno()
    sel.register(p2Conn, selectors.EVENT_READ, receive)
    p2Active = True
    print("Welcome to Fantactics.")

    bluePlayer, redPlayer = assignPlayers()

    setTurn("blue", bluePlayer.getConn(), redPlayer.getConn())

    listenSocket.close() 

    while p1Active or p2Active:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
        
    p1Conn.shutdown(socket.SHUT_RDWR)
    p1Conn.close() 

    p2Conn.shutdown(socket.SHUT_RDWR)
    p2Conn.close()
    print ('Connection Closed')