from tkinter import Tk
from graphics import Window
from gameBoard import GameBoard
from gameState import Player, GameState
from userInterface import UserInterface
from constants import *
import threading
import time
from clientConnection import *

connAlive = True
gameAlive = True

def conn_thread():
    n = 0
    while n<20 and gameAlive:
        print("Hello World: ", n)
        time.sleep(0.25)
        n+=1

def checkConn():
    if threadConn.is_alive():
        print("Connection alive")
        root.after(200, checkConn)
    else:
        root.destroy()

threadConn = threading.Thread(target=conn_thread)
if __name__ == "__main__":
    
    threadConn.start()

    root = Tk()
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, root)
    userInterface = UserInterface(root)
    board = GameBoard(window, root, userInterface)
    player1 = Player()
    player2 = Player()
    gameState = GameState(player1, player2, board, userInterface)
    root.after(200,checkConn)
    root.mainloop()
    print ("AFter mainloop")
    threadConn.join
