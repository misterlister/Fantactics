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
from errors import *

this_file = "main.py"


if __name__ == "__main__":

    connResult, conn = establishConn("localhost", 5000, 2)
    if not connResult:
        errorMessage(this_file, "Could not establish connection")
        exit()
    recv = receiver(conn)
    root = myTk()
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, root)
    userInterface = UserInterface(root)
    board = GameBoard(window, root, userInterface)
    player1 = Player()
    player2 = Player()
    gameState = GameState(player1, player2, board, userInterface)
    root.mainloop()
    lock.acquire()
    gameClosedEvent.set()
    lock.release()