from tkinter import Tk
from graphics import Window
from gameBoard import GameBoard
from gameState import Player, GameState
from userInterface import UserInterface
from constants import *
import time
from clientConnection import *
from tkWrapper import *
from errors import *
from clientSend import Sender

this_file = "main.py"


if __name__ == "__main__":

    connResult, conn = establishConn("localhost", 5000, 2)
    if not connResult:
        errorMessage(this_file, "Could not establish connection")
        exit()
    player = Player()
    opponent = Player()
    root = myTk()
    sender = Sender(conn)
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, root)
    userInterface = UserInterface(root)
    board = GameBoard(window, root, sender, userInterface)
    gameState = GameState(player, opponent, board, userInterface, sender)
    recv = receiver(conn, gameState, board)
    root.bind('<Escape>', lambda a: endfGame(a,root))

    root.mainloop()
    print("After Mainloop")
    print("After Destroy")

    gameClosedEvent.set()
    connClosedEvent.set()
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()