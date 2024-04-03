import socket
from errors import *
from constants import *

this_file = "test"

if __name__ == "__main__":    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((IP, PORT))

    except:
        errorMessage(this_file, "Could not establish connection.")
    
    print("Connected to server.")

    while True:
        data =sock.recv(MAX_MESSAGE_SIZE)

        if data:
            print(data.decode('ascii'))
        
        else:
            break
            
