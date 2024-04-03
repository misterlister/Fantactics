from constants import *
from serverRecv import *
from errors import errorMessage
import selectors
import random
from serverGameBoard import Space, GameBoard
from serverGameState import GameState, Player
import time
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

    def __init__(self, serverConn: ServerConnection):
        self.conn = serverConn 
        self.board = GameBoard()
        self.light = Player()
        self.dark = Player()
        print("Creating state")
        self.state = GameState(self.light,self.dark, self.board)
        print("state created")


    def receive_data(self,conn, mask):
        data = conn.recv(MAX_MESSAGE_SIZE)
        if data:
            message = data.decode('ascii')
            msgs = message.split()
            print("Msg: ", message)

        else:
            sel.unregister(conn)
            conn.close()

    def get_light_conn(self):
        return self.__light_conn
    
    def get_dark_conn(self):
        return self.__dark_conn
    
    def print_board(self):
        spaces = self.board.get_spaces()

        for r in range(0,len(spaces)):
            for c in range (0,len(spaces[r])):
                if spaces[r][c].get_unit() is not None:
                    print('(',r,', ',c,'): ', spaces[r][c].get_unit().get_unit_type()," -- ", spaces[r][c].get_unit().get_id())
        
        
        self.conn.get_light_conn().sendall("[Clr:BLUE]".encode('ascii'))
        self.conn.get_dark_conn().sendall("[Clr:RED]".encode('ascii'))
        time.sleep(0.25)
        self.conn.get_light_conn().sendall('[Turn:YOU]'.encode('ascii'))
        self.conn.get_dark_conn().sendall('[Turn:OPP]'.encode('ascii'))
        time.sleep(0.25)

        self.conn.get_light_conn().sendall('[Board:INIT]'.encode('ascii'))
        self.conn.get_dark_conn().sendall('[Board:INIT]'.encode('ascii'))