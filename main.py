from tkinter import Tk
from graphics import Window, WINDOW_WIDTH, WINDOW_HEIGHT
from gameBoard import GameBoard
from gameState import Player, GameState
from userInterface import UserInterface

if __name__ == "__main__":
    root = Tk()
    window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, root)
    userInterface = UserInterface(root)
    board = GameBoard(window, root, userInterface)
    
    player1 = Player()
    player2 = Player()
    gameState = GameState(player1, player2, board)
    root.mainloop()