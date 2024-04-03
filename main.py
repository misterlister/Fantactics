from tkinter import Tk
from sys import argv
from graphics import Window
from startMenu import MainMenu, create_game
from constants import *

doMainMenu = False

if __name__ == "__main__":
    for arg in argv:
        if arg == '-m':
            doMainMenu = True
    root = Tk()
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, root)

    if doMainMenu: mainMenu = MainMenu(root, window)
    else:
        create_game(root, window)
    root.mainloop()

