from tkinter import Tk
from graphics import Window, window_width, window_height

if __name__ == "__main__":
    root = Tk()
    window = Window(window_width, window_height, root)
    window.wait_for_close()