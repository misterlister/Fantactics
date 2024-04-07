import socket
from constants import *
from errors import errorMessage
import time
import random
from queue import Queue

this_file = "serverSend.py"

class ServerSender: 

    def __init__(self, serverConn):
        self.conn = serverConn

    def sendString(self,recipient, message: str):
        recipient.sendall(message.encode('ascii'))
