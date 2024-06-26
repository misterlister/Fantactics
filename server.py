import socket
import selectors
from constants import (
    MAX_MESSAGE_SIZE
)
from serverConnection import (
    ServerConnection,
    Receiver,
    sel
)
from serverSender import ServerSender
from errors import errorMessage
from gameBoard import MapLayout

this_file = "server.py"

if __name__ == "__main__":
    
    print("Welcome to the Fantactics Server.\n")


    # Initial parameters for listen socket.
    port = 5500
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    listen_socket = None

    # Try to establish listen socket. Change port if it is unavailable.
    while listen_socket is None:
        try:
            listen_socket = socket.socket()
            listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
            listen_socket.bind((ip, port))
            listen_socket.listen()
        except:
            port += 10
   
    # UDP broadcast code. This broadcasts the listen socket and port number to all clients:
    broadcast_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    broadcast_sock.settimeout(1)
    broadcast_sock.bind(("", 6000))

    # The message to be broadcast:
    message = "[HOST:" + hostname + "," + ip + "," + str(port) + "]"
    num_connections = 0

    # Keep broadcasting until we have two connections.
    while num_connections < 2:
        broadcast_sock.sendto(message.encode('ascii'), ('<broadcast>', 6100))
        print("message sent: ", message)
        data = None
        try: 
            data, addr = broadcast_sock.recvfrom(MAX_MESSAGE_SIZE)
        except:
            pass

        # If our broadcast message is echoed back to us by the client:
        if data is not None:
            if data == message.encode('ascii'):
                num_connections += 1
    # Once we've reached two clients, the loop ends and we can close this socket.
    broadcast_sock.close()
    
    # Message to users. 
    print(hostname," listenining at: ", ip, ", port: ", port)    
    
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
    layout = MapLayout()
    my_map = layout.get_random_map()
    print("CHOSEN MAP: ", my_map)
    white_msg = "[CLR:WHITE]\n [MAP:" + my_map + "]\n"
    black_msg = "[CLR:BLACK]\n [MAP:" + my_map + "]\n"
    sender.sendString(serverConn.get_white_conn(), white_msg)
    sender.sendString(serverConn.get_black_conn(), black_msg)

    if p1_active and p2_active:
        receiver.set_connection_active()

    # Register the file opjects for each connections with receive_data as the callback.
    sel.register(conn1, selectors.EVENT_READ, receiver.receive_data)
    sel.register(conn2, selectors.EVENT_READ, receiver.receive_data)
    
    # Both players are connected to new sockets, so listen socket is closed.
    listen_socket.close() 

    # Keep listening while both connections are active. 
    while receiver.is_connection_active():
        try:
            events = sel.select()
        except:
            break
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)
    
    #Close both connections, since we're done with them.
    conn1.close() 
    conn2.close()

    print ('Connection Closed')
