from tkinter import Tk
from graphics import Window, window_width, window_height
from gameBoard import GameBoard
from gameState import Player, GameState
from userInterface import ControlPanel

if __name__ == "__main__":
    root = Tk()
    window = Window(window_width, window_height, root)
    controlPanel = ControlPanel(window, root)
    board = GameBoard(window, root)
    
    player1 = Player()
    player2 = Player()
    gameState = GameState(player1, player2, board)
    root.mainloop()