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

    def get_white_conn(self):
        return self.__light_conn
    
    def get_black_conn(self):
        return self.__dark_conn
       
    def get_white_fileno(self):
        return self.__light_id
    
    def get_black_fileno(self):
        return self.__dark_id
    

class Receiver:

    def __init__(self, serverConn: ServerConnection, sender: ServerSender):
        self.conn = serverConn 
        self.sender = sender
        self.white_ready = False
        self.black_ready = False

    def receive_data(self,conn, mask):

        data = conn.recv(MAX_MESSAGE_SIZE)

        if data:
            if conn.fileno() == self.conn.get_white_fileno():
                receiver = self.conn.get_black_conn()
                sender = self.conn.get_white_conn()
                msg_sender = "white"

            if conn.fileno() == self.conn.get_black_fileno():
                receiver = self.conn.get_white_conn()
                sender = self.conn.get_black_conn()

                msg_sender = "black"


            message = data.decode('ascii')
            message = message.strip()
            
            print("Msg:", message)
            
            if(message == "[RDY]"):
                if msg_sender == "white":
                    self.white_ready = True

                if msg_sender == "black":
                    self.black_ready = True

                if self.white_ready and self.black_ready:
                    self.sender.sendString(sender,"[RDY]")
                    self.sender.sendString(receiver,"[RDY]")
            
            if(message == "[ENDTURN]"):
                self.sender.sendString(receiver,"[YOURTURN]")
                
        else:
            sel.unregister(conn)
            conn.close()
