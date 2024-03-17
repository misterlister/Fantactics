import socket
import sys
IP = 'localhost'
PORT = 5000  
MAX_MESSAGE_SIZE = 256


if __name__ == "__main__":

    listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSocket.bind((IP,PORT))
    listenSocket.listen()
    print('Listening Socket Established. Clients can connect to: ',socket.gethostname()," on port ", PORT, ".")

    p1Connection, p1Address = listenSocket.accept()
    print("Player 1 has connected.")
    p1Connection.sendall('P1: Welcome to the server, player 1\n\n'.encode('ascii'))


    while True: # While player 1 has not connected:

            try:
                data = p1Connection.recv(MAX_MESSAGE_SIZE)
            except:
                break
            msg = data.decode('ascii')
            print("Player 1 sent: ", msg)
            response = "You sent: " + msg 
        
    p1Connection.shutdown(socket.SHUT_RDWR)
    p1Connection.close() 
    print ('Connection Closed')