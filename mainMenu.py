from graphics import Window, Point
from tkinter import Tk, Label
from PIL import ImageTk, Image
from userInterface import Panel, CanvasButton
from constants import *

class MainMenu(Panel):
    def __init__(
            self, 
            root: Tk, 
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

        self.titleImg = ImageTk.PhotoImage(Image.open('Assets/Text/fantactics_title.png'))
        self.title = Label(self.frame, image=self.titleImg, bg=bgColour)
        self.title.place(x=width/2, y=height/8, anchor='n')

        self.buttons = {
            'play' : CanvasButton(self.frame, unpressed='Assets/Text/play_unpressed.png', pressed='Assets/Text/play_pressed.png'),
            'options' : CanvasButton(self.frame, unpressed='Assets/Text/options_unpressed.png'), #unpressed='Assets/Text/options_pressed.png'),
            'exit' : CanvasButton(self.frame, unpressed='Assets/Text/exit_unpressed.png') #, self.assets['exit_pressed'])
        }

        index = 160
        for item in self.buttons:
            self.buttons[item].get_button().config(bg=bgColour)
            self.buttons[item].get_button().place(x=width / 2, y=(height / 8) + index, anchor='n')
            index += 90
