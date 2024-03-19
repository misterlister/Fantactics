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
    player = Player()
    opponent = Player()
    root = myTk()
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, root)
    userInterface = UserInterface(root)
    board = GameBoard(window, root, userInterface)
    gameState = GameState(player, opponent, board, userInterface)

    recv = receiver(conn, player, opponent,gameState)

    root.mainloop()
    lock.acquire()
    gameClosedEvent.set()
    lock.release()