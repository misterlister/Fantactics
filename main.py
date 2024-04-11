from tkinter import Tk
from sys import argv
from graphics import Window
from startMenu import StartMenu, Game
from constants import *
from errors import errorMessage
from clientConnection import Receiver, establishConn
from clientSender import Sender
import socket

doMainMenu = True
online = True
sender = None
conn = None
hostname = None
port = None
this_file = "main.py"

if __name__ == "__main__":
    
    map = None
    for arg in argv:
        if arg == '-g':
            doMainMenu = False
        if arg == '-o':
            online = False
        if arg.startswith("-h:"):
            args = arg.split(":")
            print(args)
            if len(args) == 3:
                hostname = args[1]
                port = int(args[2])
        if arg.startswith("-m:"):
            map = arg[3:]
        
    if online:
        if hostname == None:
            hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        if port == None:
            port = 5000
        online = True
        connResult, conn = establishConn(ip_address, port)
        if not connResult:
            online = False
        else:
            sender = Sender(conn)

    root = Tk()
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, root)
    game = Game(root, window, sender)
    mainMenu = StartMenu(root, window, game, sender, online)
    if online:
        receiver = Receiver(conn, mainMenu)

    root.mainloop()

