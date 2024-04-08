import random
import os
from tkinter import Tk, Label, Canvas
from PIL import ImageTk, Image
from userInterface import CanvasButton, ToggleButton
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    EMPTY_SPRITE
)
from graphics import Window
from gameBoard import GameBoard
from gameState import Player, GameState
from userInterface import UserInterface

maxScale = 2.0
floatRange = 10.0
speedRange = 2.00
numSprites = 5
bound = int(WINDOW_WIDTH/3)

class Game():
    def __init__(self, root, window) -> None:
        self.userInterface = UserInterface(root)
        self.board = GameBoard(window, root, self.userInterface)
        self.player1 = Player("white")
        self.player2 = Player("black")
        self.gameState = GameState(self.player1, self.player2, self.board, self.userInterface)

class StartMenu():
    def __init__(
            self, 
            root: Tk,
            window: Window, 
            width: int = WINDOW_WIDTH, 
            height: int = WINDOW_HEIGHT, 
            bgColour: str = 'black',
            online: bool = False
            ) -> None:
        self.root = root
        self.enabled = True
        self.online = online
        self.width = width
        self.height = height
        self.bgColour = bgColour
        self.canvas = Canvas(self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='black', bd=0, highlightthickness=0)
        self.canvas.pack_propagate(0)
        self.canvas.place(x=0, y=0)
        self.backgroundImage = ImageTk.PhotoImage(Image.open('Assets/title_background.png'))
        self.background = self.canvas.create_image(0, 0, image=self.backgroundImage, anchor='nw')

        self.waiting = [
            ImageTk.PhotoImage(Image.open('Assets/Text/Waiting_1.png')),
            ImageTk.PhotoImage(Image.open('Assets/Text/Waiting_2.png')),
            ImageTk.PhotoImage(Image.open('Assets/Text/Waiting_3.png')),
            
        ]
        self.sprites = [[],[]]
        self.img = [[],[]]
        self.speed = [[],[]]

        for i in range(numSprites):
            self.sprites[0].append(self.canvas.create_image(random.randint(0, bound), random.uniform(1.0, floatRange) * -60, anchor='nw'))
            self.img[0].append(ImageTk.PhotoImage(Image.open(EMPTY_SPRITE)))

            self.speed[0].append(random.uniform(1.00, speedRange))

            self.sprites[1].append(self.canvas.create_image(random.randint(2 * bound, WINDOW_WIDTH), random.uniform(1.0, floatRange) * -60, anchor='ne'))
            self.img[1].append(ImageTk.PhotoImage(Image.open(EMPTY_SPRITE)))
            self.speed[1].append(random.uniform(1.00, speedRange))

        for index, item in enumerate(self.sprites[0]):
            self.change_image(item, index, 0)
            self.animate(item, index, 0)

        for index, item in enumerate(self.sprites[1]):
            self.change_image(item, index, 1)
            self.animate(item, index, 1)

        self.window = window
        self.titleImg = ImageTk.PhotoImage(Image.open('Assets/Text/fantactics_title.png'))
        self.title = self.canvas.create_image(WINDOW_WIDTH/2, height/8, image=self.titleImg, anchor='n')

        self.buttons = {
            'play' : CanvasButton(self.canvas, unpressed='Assets/Text/play_unpressed.png', pressed='Assets/Text/play_pressed.png'),
            'options' : CanvasButton(self.canvas, unpressed='Assets/Text/options_unpressed.png', pressed='Assets/Text/options_pressed.png'),
            'exit' : CanvasButton(self.canvas, unpressed='Assets/Text/exit_unpressed.png', pressed='Assets/Text/exit_pressed.png')
        }

        self.index = 160
        # Bind clicks to buttons & set their position
        self.place_buttons(self.index)
        self.buttons['play'].change_unclick_func(self.play)
        self.buttons['options'].change_unclick_func(self.options)
        self.buttons['exit'].change_unclick_func(self.exit)

        self.currentMenu = 0

    def animate(self, sprite, index, colour):
        if self.enabled:
            loc = self.canvas.coords(sprite)
            if loc[1] > WINDOW_HEIGHT:
                self.speed[colour][index] = random.uniform(1.00, speedRange)
                self.change_image(sprite, index, colour)
                if colour == 0:
                    self.canvas.moveto(sprite, random.randint(0, bound), random.uniform(1.0, 3.0) * (-100 * self.scale))
                else:
                    self.canvas.moveto(sprite, random.randint(2 * bound, WINDOW_WIDTH - 50), random.uniform(1.0, 3.0) * (-100 * self.scale))
            self.canvas.move(sprite, 0, self.speed[colour][index])
            self.root.after(16, self.animate, sprite, index, colour)

    def get_random_sprite(self, colour):
        if colour == 0:
            unitDir = 'Assets/Units/White'
        else:
            unitDir = 'Assets/Units/Black'
        files = os.listdir(unitDir)
        number = random.randint(0, len(files) - 1)
        image = files[number]
        return f"{unitDir}/{image}"
    
    def change_image(self, sprite, index, colour):
        image = self.get_random_sprite(colour)
        load = Image.open(image)
        self.scale = random.uniform(1, maxScale)
        load = load.resize((int((16 * 4) * self.scale), int((17 * 4) * self.scale)), Image.LANCZOS)
        self.img[colour][index] = ImageTk.PhotoImage(load)
        self.canvas.itemconfig(sprite, image=self.img[colour][index])

    def place_buttons(self, index):
        for item in self.buttons:
            item = self.buttons[item]
            item.bind(item.click, item.unclick)
            item.get_button().config(bg=self.bgColour)
            item.get_button().place(x=WINDOW_WIDTH/2, y=(self.height / 8) + index, anchor='n')
            index += 90
    
    def hide_buttons(self):
        for item in self.buttons:
                self.buttons[item].hide()

    def back_button(self):
        self.backBtn = CanvasButton(self.canvas, bg=self.bgColour, unpressed='Assets/Text/back_unpressed.png', pressed='Assets/Text/back_pressed.png')
        self.backBtn.place(WINDOW_WIDTH/2, self.height/8 + 360, anchor='n')
        self.backBtn.change_unclick_func(self.back)
         
    def play(self):
        if self.online:
            self.currentMenu = 1
            self.hide_buttons()
            self.back_button()

            self.waitImg = self.canvas.create_image(WINDOW_WIDTH/2, self.height/8 + 160, image=self.waiting[0])
            self.currentImg = 3
            self.waitingForOpponent = True
            self.wait_anim()

            ### For Glen to add here --- Once both players are connected, call load_game()

        else:
            self.load_game()

    def wait_anim(self):
        if self.waitingForOpponent:
            if self.currentImg == 1:
                self.currentImg = 2
                self.canvas.itemconfig(self.waitImg, image=self.waiting[1])
            elif self.currentImg == 2:
                self.currentImg = 3
                self.canvas.itemconfig(self.waitImg, image=self.waiting[2])
            elif self.currentImg == 3:
                self.currentImg = 1
                self.canvas.itemconfig(self.waitImg, image=self.waiting[0])
            
            self.root.after(1000, self.wait_anim)

    def load_game(self):
        Game(self.root, self.window)
        self.enabled = False
        self.canvas.destroy()

    def options(self):
        self.currentMenu = 2
        self.hide_buttons()
        self.back_button()
        self.onlineBtn = ToggleButton(self.canvas, bg=self.bgColour, disable=False, unpressed='Assets/Text/online_unpressed.png', pressed='Assets/Text/online_pressed.png')
        self.toggleKey = [self.onlineBtn]
        self.onlineBtn.set_key(self.toggleKey)
        self.onlineBtn.change_unclick_func(self.toggle_online)
        if self.online:
            self.onlineBtn.toggle()
        self.onlineBtn.place(WINDOW_WIDTH/2, self.height/8 + 270, anchor='n')
    
    def toggle_online(self):
        if self.online == True:
            self.online = False
            print(self.online)
        else: 
            self.online = True
        
    def back(self):
        self.backBtn.destroy()
        if self.currentMenu == 1: 
            self.canvas.delete(self.waitImg)
            self.waitingForOpponent = False
        elif self.currentMenu == 2: self.onlineBtn.destroy()
        self.place_buttons(self.index)
        self.currentMenu = 0

    def exit(self):
        self.enabled = False
        self.root.destroy()
