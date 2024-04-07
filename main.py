from tkinter import Tk
from sys import argv
from graphics import Window
from startMenu import StartMenu, Game
from constants import *
from errors import errorMessage
from clientConnection import Receiver, establishConn

this_file = "main.py"
doMainMenu = False

if __name__ == "__main__":

    connResult, conn = establishConn(IP, PORT)
    
    if not connResult:
        errorMessage(this_file, "Could not establish connection")
        exit()

    root = Tk()
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, root)
    game = Game(root,window)
    receiver = Receiver(conn,game)
    mainMenu = StartMenu(root, window,game)

    root.mainloop()

