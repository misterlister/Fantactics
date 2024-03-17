from tkinter import Tk
import threading

root = Tk()
lock = threading.Lock()
gameClosedEvent = threading.Event()
connClosedEvent = threading.Event()
myTurn = False

