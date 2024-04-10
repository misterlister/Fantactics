from tkinter import Tk
from sys import argv
from graphics import Window
from startMenu import StartMenu, Game
from constants import *

doMainMenu = False
online = False

if __name__ == "__main__":
    map = None
    for arg in argv:
        if arg == '-g':
            doMainMenu = True
        if arg == '-o':
            online = True
        if arg.startswith("-m:"):
            map = arg[3:]

    root = Tk()
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, root)

    if doMainMenu: mainMenu = StartMenu(root, window, online=online, map=map)
    else: game = Game(root, window)
    root.mainloop()

