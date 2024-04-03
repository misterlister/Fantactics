from tkinter import Tk
from sys import argv
from graphics import Window
from gameBoard import GameBoard
from gameState import Player, GameState
from userInterface import UserInterface
from mainMenu import MainMenu
from constants import *

doMainMenu = False

if __name__ == "__main__":
    for arg in argv:
        if arg == '-m':
            doMainMenu = True
    root = Tk()
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, root)
    userInterface = UserInterface(root)
    board = GameBoard(window, root, userInterface)
    player1 = Player()
    player2 = Player()
    gameState = GameState(player1, player2, board, userInterface)
    if doMainMenu: mainMenu = MainMenu(root)
    root.mainloop()