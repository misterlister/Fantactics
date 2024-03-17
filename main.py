from tkinter import Tk
from graphics import Window
from gameBoard import GameBoard
from gameState import Player, GameState
from userInterface import UserInterface
from constants import *
import time
from clientConnection import *
from globals import *
from tkWrapper import myTk

if __name__ == "__main__":

    conn = clientConnection("localhost", 5000)
    root = myTk()
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, root)
    userInterface = UserInterface(root)
    board = GameBoard(window, root, userInterface)
    player1 = Player()
    player2 = Player()
    gameState = GameState(player1, player2, board, userInterface)
    root.mainloop()
    
    conn.setConnClosed()

    conn.joinThread()
