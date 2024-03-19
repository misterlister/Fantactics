from tkinter import Tk
from clientConnection import *
import time
from globals import *
class myTk(Tk):
    
    def __init__(self):
        super().__init__()
        gameClosedEvent.clear()
        self.after(250,self.__checkConn)

    def __checkConn(self):

        if  not connClosedEvent.is_set():
            self.after(500, self.__checkConn)
        else:
            self.__onConnectionClose()

    def __onConnectionClose(self):
        self.destroy()


