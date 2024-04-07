from constants import *
from errors import errorMessage
import selectors
import random

from serverSender import ServerSender
import time

this_file = "ServerConnection.py"

p1_active = False
p2_active = False
sel = selectors.DefaultSelector()
    
class ServerConnection:
    def __init__(self, conn1, conn2):

        random_number = random.randint(1,100)
        
        if random_number%2 == 0:
            self.__light_conn = conn1
            self.__dark_conn = conn2

        else:
            self.__light_conn = conn2
            self.__dark_conn = conn1

        self.__light_id = self.__light_conn.fileno()
        self.__dark_id = self.__dark_conn.fileno()

    def get_light_conn(self):
        return self.__light_conn
    
    def get_dark_conn(self):
        return self.__dark_conn
    

class Receiver:

    def __init__(self, serverConn: ServerConnection, sender: ServerSender):
        self.conn = serverConn 
        self.sender = sender

    def receive_data(self,conn, mask):
        data = conn.recv(MAX_MESSAGE_SIZE)
        if data:
            message = data.decode('ascii')
            msgs = message.split()
            print("Msg: ", message)

        else:
            sel.unregister(conn)
            conn.close()
