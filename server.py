import socket
import selectors
from constants import *
from serverConnection import *
from serverSender import ServerSender
from errors import errorMessage

this_file = "server.py"

if __name__ == "__main__":
    

    # Create socket to listen for incoming connections
    listen_socket = socket.socket()
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    listen_socket.bind((IP, PORT))
    listen_socket.listen()

    # Message to users. 
    print("Server listenining at hostname: ", IP, ", port: ", PORT)    
    
    # Accept the first connection.
    try:
        conn1, addr1 = listen_socket.accept()
        p1_active = True

    except:
        errorMessage(this_file,"Could not establish connection with player 1.")


    #Accept the second connection.
    try:
        conn2, addr2 = listen_socket.accept()
        p2_active = True

    except:
        errorMessage(this_file,"Could not establish connection with player 2.")

    # Assign each connection to be randomly either the light or dark player.
    serverConn = ServerConnection(conn1, conn2)
    sender = ServerSender(serverConn)
    receiver = Receiver(serverConn, sender)
    
    sender.sendString(serverConn.get_white_conn(), "[CLR:WHITE]")
    sender.sendString(serverConn.get_black_conn(), "[CLR:BLACK]")

    # Register the file opjects for each connections with receive_data as the callback.
    sel.register(conn1, selectors.EVENT_READ, receiver.receive_data)
    sel.register(conn2, selectors.EVENT_READ, receiver.receive_data)
    
    # Both players are connected to new sockets, so listen socket is closed.
    listen_socket.close() 

    # Keep listening while both connections are active. 
    while p1_active or p2_active:
        try:
            events = sel.select()
        except:
            break
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
        
    conn1.close() 
    conn2.close()

    print ('Connection Closed')
