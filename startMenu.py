import random
import os
from tkinter import Tk, Label, Canvas
from PIL import ImageTk, Image
from userInterface import CanvasButton, ToggleButton
from constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    EMPTY_SPRITE,
    P1_COL,
    P2_COL,
    CPU_Difficulty
)
from graphics import Window
from gameBoard import GameBoard
from gameState import GameState
from player import Player, CPU_Player
from userInterface import UserInterface
from clientSender import Sender

maxScale = 2.0
floatRange = 10.0
speedRange = 2.00
numSprites = 5
bound = int(WINDOW_WIDTH/3)

class Game():
    def __init__(self, root, window, sender, map = None) -> None:
        self.root = root
        self.window = window
        self.sender = sender
        self.player_colour = None
        self.player1 = None
        self.player2 = None
        self.userInterface = None
        self.board = None
        self.state = None
        self.map = map
        
    def start(self):
        self.userInterface = UserInterface(self.root)
        self.board = GameBoard(self.window, self.root, self.userInterface, self.player_colour, self.sender)
        if self.player_colour == P1_COL:
            self.player1 = Player(P1_COL)
            self.player2 = Player(P2_COL)
        else:
            self.player1 = Player(P2_COL)
            self.player2 = Player(P1_COL)
        self.state = GameState(self.player1, self.player2, self.board, self.userInterface, self.map, self.sender)

    def set_player_colour(self, colour:str):
        self.player_colour = colour

    def set_map(self, map: str):
        self.map = map

    def start_one_player(self, is_cpu_game: bool):
        self.userInterface = UserInterface(self.root)
        # If this is a cpu game, randomly pick the player colour
        if is_cpu_game:
            if random.randint(0, 1) == 1:
                # cpu is Player 1
                player = P2_COL
                cpu = P1_COL
            else:
                # cpu is Player 2
                player = P1_COL
                cpu = P2_COL
            self.player1 = Player(player)
            self.player2 = CPU_Player(cpu, difficulty=CPU_Difficulty.Medium)
        else:
            self.player1 = Player(P1_COL)
            self.player2 = Player(P2_COL)
            
        self.board = GameBoard(self.window, self.root, self.userInterface, P1_COL, None)

        self.state = GameState(self.player1, self.player2, self.board, self.userInterface, self.map, None, is_cpu_game)


class StartMenu():
    def __init__(
            self, 
            root: Tk,
            window: Window, 
            game: Game,
            sender: Sender,
            online: bool,
            width: int = WINDOW_WIDTH, 
            height: int = WINDOW_HEIGHT, 
            bgColour: str = 'black',
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
        self.map = map
        self.cpu_game = True # Default to False

        self.credImg = [
            ImageTk.PhotoImage(Image.open('Assets/Text/hayden.png')),
            ImageTk.PhotoImage(Image.open('Assets/Text/glen.png')),
            ImageTk.PhotoImage(Image.open('Assets/Text/shane.png')),
        ]
        self.cred = []

        self.waiting = [
            ImageTk.PhotoImage(Image.open('Assets/Text/waiting_1.png')),
            ImageTk.PhotoImage(Image.open('Assets/Text/waiting_2.png')),
            ImageTk.PhotoImage(Image.open('Assets/Text/waiting_3.png')),
            
        ]
        self.sprites = [[],[]]
        self.img = [[],[]]
        self.speed = [[],[]]
        self.game = game
        self.sender = sender
        self.waitingForOpponent = True

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
        
        self.onlineIndImg = ImageTk.PhotoImage(Image.open("Assets/Text/online_pressed.png"))
        self.offlineIndImg = ImageTk.PhotoImage(Image.open("Assets/Text/online_unpressed.png"))

        if self.online:
            self.onlineInd = self.canvas.create_image(WINDOW_WIDTH - 60, 20, image=self.onlineIndImg, anchor='ne')
        if not self.online:
            self.onlineInd = self.canvas.create_image(WINDOW_WIDTH - 60, 20, image=self.offlineIndImg, anchor='ne')


        self.buttons = {
            'play' : CanvasButton(self.canvas, unpressed='Assets/Text/play_unpressed.png', pressed='Assets/Text/play_pressed.png'),
            'credits' : CanvasButton(self.canvas, unpressed='Assets/Text/credits_unpressed.png', pressed='Assets/Text/credits_pressed.png'),
            'exit' : CanvasButton(self.canvas, unpressed='Assets/Text/exit_unpressed.png', pressed='Assets/Text/exit_pressed.png')
        }

        self.index = 160
        # Bind clicks to buttons & set their position
        self.place_buttons(self.index)
        self.buttons['play'].change_unclick_func(self.play)
        self.buttons['credits'].change_unclick_func(self.credits)
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

    def back_button(self, x=WINDOW_WIDTH/2, y=720 - 200):
        self.backBtn = CanvasButton(self.canvas, bg=self.bgColour, unpressed='Assets/Text/back_unpressed.png', pressed='Assets/Text/back_pressed.png')
        self.backBtn.place(x, y, anchor='n')
        self.backBtn.change_unclick_func(self.back)
         
    def play(self):

        if not self.online:
            self.start()

        else:
            self.sender.send("[RDY]")

            if not self.waitingForOpponent:
                self.start_online()
            else:
                self.waitImg = self.canvas.create_image(WINDOW_WIDTH/2, self.height/8 + 160, image=self.waiting[0])
                self.currentImg = 3
                self.waitImg = self.canvas.create_image(WINDOW_WIDTH/2, self.height/8 + 160, image=self.waiting[0])
                self.currentImg = 3
                self.waitingForOpponent = True
                self.currentMenu = 1
                self.hide_buttons()
                self.wait_anim()

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
            self.sender.send("[RDY]")
            self.root.after(500, self.wait_anim)
        else:
            self.start_online()

    def credits(self):
        self.currentMenu = 3
        
        index = 50
        for img in self.credImg:
            self.cred.append(self.canvas.create_image(WINDOW_WIDTH/2, self.index + index, image=img, anchor='n'))
    
            index += 150
        self.hide_buttons()
        self.back_button(y=self.height - 60)
    
    def toggle_online(self):
        if self.online == True:
            self.online = False
        else: 
            self.online = True
        
    def back(self):
        self.backBtn.destroy()
        if self.currentMenu == 1: 
            self.canvas.delete(self.waitImg)
            self.waitingForOpponent = False
        elif self.currentMenu == 2: self.onlineBtn.destroy()
        elif self.currentMenu == 3: 
            for item in self.cred:
                self.canvas.delete(item)
        self.place_buttons(self.index)
        self.currentMenu = 0

    def exit(self):
        self.enabled = False
        self.root.destroy()

    def start(self):
        self.enabled = False
        self.canvas.destroy()
        self.game.start_one_player(self.cpu_game)

    def start_online(self):
        self.enabled = False
        self.canvas.destroy()
        self.game.start()

    def setOpponentReady(self):
        self.waitingForOpponent = False
