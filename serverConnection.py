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
        
        data = None
        try:
            data = conn.recv(MAX_MESSAGE_SIZE)
        
        except:
            errorMessage(this_file,"Connection was closed")
        if data is not None:
            if conn.fileno() == self.conn.get_white_fileno():
                receiver = self.conn.get_black_conn()
                sender = self.conn.get_white_conn()
                msg_sender = "white"

            if conn.fileno() == self.conn.get_black_fileno():
                receiver = self.conn.get_white_conn()
                sender = self.conn.get_black_conn()
                msg_sender = "black"


            messages = data.decode('ascii').split()

            for msg in messages:

                print("Msg:", msg)
                
                if(msg == "[RDY]"):
                    if msg_sender == "white":
                        self.white_ready = True

                    if msg_sender == "black":
                        self.black_ready = True

                    if self.white_ready and self.black_ready:
                        self.sender.sendString(sender,"[RDY]")
                        self.sender.sendString(receiver,"[RDY]")
                
                #if(msg == "[ENDTURN]"):
                    #self.sender.sendString(receiver,"[YOURTURN]")
                
                if(msg[1:5]=="MOVE"):
                    move_str = msg[6:-1]
                    move_params = move_str.split(",")

                    new_msg = "[MOVE:" + move_params[0] + ","
                    for i in range(1,7):
                        new_msg += (str(abs(int(move_params[i])-7))) 
                        if i < 6:
                            new_msg += ","                            

                    new_msg += "]"
                    print("Outgoing MEssage: ", new_msg)
                    self.sender.sendString(receiver,new_msg)

                if(msg[1:5]=="ATTK"):
                    attk_str = msg[6:-1]
                    params = attk_str.split(",")

                    new_msg = "[ATTK:" + params[0] + ","
                    for i in range(1,7):
                        new_msg += (str(abs(int(params[i])-7))) 
                        if i < 6:
                            new_msg += ","                            

                    new_msg += "]"
                    self.sender.sendString(receiver,new_msg)

    
                if(msg[1:5]=="ABIL"):
                    abil_str = msg[6:-1]
                    params = abil_str.split(",")

                    new_msg = "[ABIL:" + params[0] + ","
                    for i in range(1,7):
                        new_msg += (str(abs(int(params[i])-7))) 
                        if i < 6:
                            new_msg += ","                            

                    new_msg += "]"
                    self.sender.sendString(receiver,new_msg)



 
        else:
            sel.unregister(conn)
            conn.close()
