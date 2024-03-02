from tkinter import Tk
from graphics import Window, window_width, window_height
from gameBoard import GameBoard

if __name__ == "__main__":
    root = Tk()
    window = Window(window_width, window_height, root)
    board = GameBoard(window, root)
    root.mainloop()