from tkinter import Tk
from clientConnection import *
import time
class myTk(Tk):
    
    def __init__(self):
        super().__init__()
        setGameOpen()
        self.after(250,self.__checkConn)

    def __checkConn(self):
        
        if  not (connClosedEvent.is_set() or gameClosedEvent.is_set()):
            self.after(500, self.__checkConn)
        else:
            endfGame(-1,self)

def endfGame(event,root):
    gameClosedEvent.set()
    root.destroy()

    


