from tkinter import Tk
from sys import argv
from graphics import Window
from startMenu import StartMenu, Game
from constants import *
from errors import errorMessage
from clientConnection import Receiver, establishConn
from clientSender import Sender

doMainMenu = True
online = False
this_file = "main.py"

if __name__ == "__main__":
    onlineAvailable = True
    connResult, conn = establishConn(IP, PORT)
    if not connResult:
        errorMessage(this_file, "Could not establish connection")
        onlineAvailable = False

    map = "Great_Plains"

    for arg in argv:
        if arg == '-g':
            doMainMenu = False
        if arg == '-o':
            online = True
        if arg.startswith("-m:"):
            map = arg[3:]

    root = Tk()
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, root)
    sender = Sender(conn)
    game = Game(root,window,sender)
    mainMenu = StartMenu(root, window, game, sender, onlineAvailable)
    receiver = Receiver(conn,mainMenu)

    #if doMainMenu: mainMenu = StartMenu(root, window, game, sender, online=online, map=map)
    #else: game = Game(root, window, map=map)
    root.mainloop()

