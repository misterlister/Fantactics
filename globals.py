from tkinter import Tk
import threading

lock = threading.Lock()
gameClosedEvent = threading.Event()
connClosedEvent = threading.Event()

myTurn = False

