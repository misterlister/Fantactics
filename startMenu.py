from tkinter import Tk, Label
from PIL import ImageTk, Image
from userInterface import Panel, CanvasButton
from constants import *
from graphics import Window
from gameBoard import GameBoard
from gameState import Player, GameState
from userInterface import UserInterface

class Game():
    def __init__(self, root, window) -> None:
        self.userInterface = UserInterface(root)
        self.board = GameBoard(window, root, self.userInterface)
        self.player1 = Player()
        self.player2 = Player()
        self.gameState = GameState(self.player1, self.player2, self.board, self.userInterface)

class StartMenu(Panel):
    def __init__(
            self, 
            root: Tk,
            window: Window, 
            xPos: int = 0, 
            yPos: int = 0, 
            width: int = WINDOW_WIDTH, 
            height: int = WINDOW_HEIGHT, 
            bgColour: str = 'black',
            bd: int = 0,
            relief: str = 'solid',
            textColour: str = 'white',
            ) -> None:
        super().__init__(root, xPos, yPos, width, height, bgColour, bd, relief)
        self.window = window
        self.titleImg = ImageTk.PhotoImage(Image.open('Assets/Text/fantactics_title.png'))
        self.title = Label(self.frame, image=self.titleImg, bg=bgColour)
        self.title.place(x=width/2, y=height/8, anchor='n')

        self.buttons = {
            'play' : CanvasButton(self.frame, unpressed='Assets/Text/play_unpressed.png', pressed='Assets/Text/play_pressed.png'),
            'options' : CanvasButton(self.frame, unpressed='Assets/Text/options_unpressed.png'), #pressed='Assets/Text/options_pressed.png'),
            'exit' : CanvasButton(self.frame, unpressed='Assets/Text/exit_unpressed.png') #, self.assets['exit_pressed'])
        }

        index = 160
        # Bind clicks to buttons & set their position
        for item in self.buttons:
            item = self.buttons[item]
            item.bind(item.click, item.unclick)
            item.get_button().config(bg=bgColour)
            item.get_button().place(x=width / 2, y=(height / 8) + index, anchor='n')
            index += 90

        self.buttons['play'].change_unclick_func(self.play)
        self.buttons['exit'].change_unclick_func(self.exit)
        

    def play(self):
        Game(self.root, self.window)
        self.frame.destroy()

    def options(self):
        pass

    def exit(self):
        self.root.destroy()

    

