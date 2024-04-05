import random
import os
from tkinter import Tk, Label, Canvas
from PIL import ImageTk, Image
from userInterface import Panel, CanvasButton
from constants import *
from graphics import Window
from gameBoard import GameBoard
from gameState import Player, GameState
from userInterface import UserInterface

maxScale = 2.0
floatRange = 10.0
speedRange = 2.00
numSprites = 5

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
        self.enabled = True
        self.canvas = Canvas(self.root, width=WINDOW_WIDTH/2, height=WINDOW_HEIGHT, bg='black', bd=0, highlightthickness=0)
        self.canvas.pack_propagate(0)
        self.canvas.place(x=(WINDOW_WIDTH / 2) + 45, y=0)
        self.sprites = []
        self.img = []
        self.speed = []

        for i in range(numSprites):
            self.sprites.append(self.canvas.create_image(random.randint(0, int((WINDOW_WIDTH / 2)- 150)), random.uniform(1.0, floatRange) * -60, anchor='nw'))
            self.img.append(ImageTk.PhotoImage(Image.open(EMPTY_SPRITE)))
            self.speed.append(random.uniform(1.00, speedRange))

        for index, item in enumerate(self.sprites):
            self.change_image(item, index)
            self.animate(item, index)

        self.window = window
        self.titleImg = ImageTk.PhotoImage(Image.open('Assets/Text/fantactics_title.png'))
        self.title = Label(self.frame, image=self.titleImg, bg=bgColour)
        self.title.place(x=10, y=height/8, anchor='nw')

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
            item.get_button().place(x=20, y=(height / 8) + index, anchor='nw')
            index += 90

        self.buttons['play'].change_unclick_func(self.play)
        self.buttons['exit'].change_unclick_func(self.exit)

    def animate(self, sprite, index):
        if self.enabled:
            loc = self.canvas.coords(sprite)
            if loc[1] > WINDOW_HEIGHT:
                self.speed[index] = random.uniform(1.00, speedRange)
                self.change_image(sprite, index)
                self.canvas.moveto(sprite, random.randint(0, int((WINDOW_WIDTH / 2) - 150)), random.uniform(1.0, 3.0) * (-100 * self.scale))
            self.canvas.move(sprite, 0, self.speed[index])
            self.root.after(16, self.animate, sprite, index)

    def get_random_sprite(self):
        unitDir = 'Assets/Units'
        files = os.listdir('Assets/Units')
        number = random.randint(0, len(files) - 1)
        image = files[number]
        return f"{unitDir}/{image}"
    
    def change_image(self, sprite, index):
        image = self.get_random_sprite()
        print(image)
        load = Image.open(image)
        self.scale = random.uniform(1, maxScale)
        load = load.resize((int((16 * 4) * self.scale), int((17 * 4) * self.scale)), Image.LANCZOS)
        self.img[index] = ImageTk.PhotoImage(load)
        self.canvas.itemconfig(sprite, image=self.img[index])

    def play(self):
        Game(self.root, self.window)
        self.enabled = False
        self.canvas.destroy()
        self.frame.destroy()

    def options(self):
        pass

    def exit(self):
        self.enabled = False
        self.root.destroy()

    

