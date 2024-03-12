from tkinter import Tk, LabelFrame, Canvas, Text, Label, Scrollbar
from PIL import ImageTk, Image
from typing import Callable
from graphics import WINDOW_WIDTH, WINDOW_HEIGHT

SPRITE_BUFFER = 8
STATS_IMAGE_SIZE = (2 * 64) + SPRITE_BUFFER
ERROR_UNPRESSED, ERROR_PRESSED = "Assets/Text/error_unpressed.png", "Assets/Text/error_pressed.png"
EMPTY_SPRITE = "Assets/Text/empty.png"
FONT = 'placeholder'
BGCOLOUR = '#5d4037'
BORDER_WIDTH = 4
PANEL_WIDTH, PANEL_HEIGHT = 320, 720 
CONTROL_PANEL_HEIGHT = 80

# It does nothing
def do_nothing(): 
    pass
    
class UserInterface():
    def __init__(self, root: Tk):

        # Create Stats Panel (left side panel)
        self.stats = Panel(root)
        self.statsPanel = { # Stats panel is divided into 3 seperate subPanels
            'friendlyUnitPanel' : StatsPanel(self.stats.getFrame(), height=PANEL_HEIGHT / 3, bgColour='#754239'),
            'enemyUnitPanel' : StatsPanel(self.stats.getFrame(), yPos=PANEL_HEIGHT / 3, height=PANEL_HEIGHT / 3, bgColour='#57312a'),
            'terrainPanel' : Panel(self.stats.getFrame(), yPos=(PANEL_HEIGHT / 3) * 2, height=PANEL_HEIGHT / 3, colour='black')
        }
        
        ### Create Log Panel (right side panel)
        self.log = Panel(root, WINDOW_WIDTH-PANEL_WIDTH, 0)
        self.logItems = {
            'text' : CombatLog(self.log.getFrame())
        }

        self.controlBar = ControlBar(root, PANEL_WIDTH, PANEL_HEIGHT - CONTROL_PANEL_HEIGHT, width=WINDOW_WIDTH - (2 * PANEL_WIDTH), height=CONTROL_PANEL_HEIGHT)
        
class Panel():
    def __init__(
            self, 
            root: Tk, 
            xPos: int = 0, 
            yPos: int = 0, 
            width: int = PANEL_WIDTH,
            height: int = PANEL_HEIGHT,
            colour: str = BGCOLOUR
            ) -> None:
        
        self.frame = LabelFrame(root, width = width, height = height, bg=colour, bd=0)
        self.frame.pack_propagate(0) # Prevent the LabelFrame from shrinking
        self.frame.pack(side = 'left', expand = 'True', anchor='nw', fill='both')
        self.frame.place(x=xPos, y=yPos)

    def getFrame(self):
        return self.frame
    
class StatsPanel(Panel):
    def __init__(
            self, 
            root: Tk, 
            xPos: int = 0, 
            yPos: int = 0, 
            width: int = PANEL_WIDTH, 
            height: int = PANEL_HEIGHT, 
            bgColour: str = BGCOLOUR,
            textColour: str = 'white',
            spriteBgColour: str = '#757eff'
            ) -> None:
        super().__init__(root, xPos, yPos, width, height, bgColour)

        ### Create the area for sprite to be displayed on click
        self.spriteCanvas = Canvas(self.frame, width=STATS_IMAGE_SIZE, height=STATS_IMAGE_SIZE, bg=spriteBgColour, highlightthickness=0, borderwidth=BORDER_WIDTH, relief='solid')
        self.spriteCanvas.pack_propagate(0)
        self.spriteCanvas.pack(expand=1, fill=None)
        self.spriteCanvas.place(x=0, y=21)

        # Empty default sprite for no unit selected
        self.empty = ImageTk.PhotoImage(Image.open(EMPTY_SPRITE))
        self.selectedSprite = self.spriteCanvas.create_image(SPRITE_BUFFER, SPRITE_BUFFER, anchor = 'nw', image=self.empty)

        # Label fields for stats to be displayed
        
        self.icons = {
            'health' : ImageTk.PhotoImage(Image.open('Assets/Icons/health.png')),
            'damage' : ImageTk.PhotoImage(Image.open('Assets/Icons/damage.png'))
        }
        self.labels = {
            'name' : Label(self.frame, text='Name:'),
            'class' : Label(self.frame, text='Class:'),
            'health' : Label(self.frame, text='', image=self.icons['health'], compound='left'),
            'damage' : Label(self.frame, text='', image= self.icons['damage'], compound='left'),
            'armour' : Label(self.frame, text='Armour:'),
            'movement' : Label(self.frame, text='Movement:')
        }
        
        index = 0
        for item in self.labels:
            self.labels[item].config(bg=bgColour, fg=textColour)
            self.labels[item].pack()
            self.labels[item].place(x=STATS_IMAGE_SIZE + (2 * BORDER_WIDTH) + 1, y=index)
            index += 30

        self.labels['name'].place(x=0, y=0)

    def clear(self) -> None:
        self.update_name()
        self.update_class()
        self.update_health()
        self.update_damage()
        self.update_armour()
        self.update_movement()   
        self.update_image(self.empty)

    def update_name(self, new: str = '') -> None:
        self.labels['name'].config(text= f"Name: {new}")
        
    def update_class(self, new: str = '') -> None:
        self.labels['class'].config(text= f"Class: {new}")

    def update_health(self, new: str = '') -> None:
        self.labels['health'].config(text= f" {new}")

    def update_damage(self, new: str = '') -> None:
        self.labels['damage'].config(text= f" {new}")
    
    def update_armour(self, new: str = '') -> None:
        self.labels['armour'].config(text= f"Armour: {new}")

    def update_movement(self, new: str = '') -> None:
        self.labels['movement'].config(text= f"Movement: {new}")
    
    def update_image(self, image: ImageTk) -> None:
        #image = image.resize((2 * image.width(), 2 * image.height()))
        self.spriteCanvas.itemconfig(self.selectedSprite, image=image)

# Attack, special ability, wait, cancel
# Class for bottom side control bar
class ControlBar(Panel):
    def __init__(
            self,
            root: Tk, 
            xPos: int = 0, 
            yPos: int = 0, 
            width: int = PANEL_WIDTH, 
            height: int = PANEL_HEIGHT, 
            colour: str = BGCOLOUR
            ) -> None:
        super().__init__(root, xPos, yPos, width, height, colour)

        self.buttons = {
            'green' : CanvasButton(self.frame, unpressed='Assets/Buttons/green_unpressed.png', pressed='Assets/Buttons/green_pressed.png'),
            'yellow' : CanvasButton(self.frame, unpressed='Assets/Buttons/yellow_unpressed.png', pressed='Assets/Buttons/yellow_pressed.png'),
            'red' : CanvasButton(self.frame, unpressed='Assets/Buttons/red_unpressed.png', pressed='Assets/Buttons/red_pressed.png'),
            'grey' : CanvasButton(self.frame, unpressed='Assets/Buttons/grey_unpressed.png', pressed='Assets/Buttons/grey_pressed.png')
        }

        spacing = 16
        index = 0
        for item in self.buttons:
            self.buttons[item].get_button().place(x=(48 * 3 * index) + spacing / 2 + (index * spacing), y=16)
            index += 1
                   
# Base class for buttons with a sprite
class CanvasButton():
    def __init__(
            self, 
            frame: LabelFrame, 
            xPos: int = 0, 
            yPos: int = 0,
            unpressed: str = ERROR_UNPRESSED,
            pressed: str = ERROR_PRESSED,
            clickFunc: Callable = do_nothing,
            unclickFunc: Callable = do_nothing,
            enabled: bool = True,
            ) -> None:
        
        self.button = Canvas(frame, bg=BGCOLOUR, bd=0, highlightthickness=0, cursor='hand2') # Create the button object
        self.button.pack_propagate(0) # Prevent the Canvas from shrinking
        self.button.pack(expand=1, fill=None)
        self.button.place(x=xPos, y=yPos)
        self.button.bind('<Button-1>', self.__click)
        self.button.bind('<ButtonRelease-1>', self.__unclick)
        
        self.__create_image(unpressed, pressed)
        self.currentImage = self.button.create_image(0, 0, anchor = 'nw', image=self.unpressed)

        self.__clickFunc = clickFunc
        self.__unclickFunc = unclickFunc
        

        self.enabled = enabled

    def change_image(
            self, 
            unpressed: str = ERROR_UNPRESSED, 
            pressed: str = ERROR_PRESSED
            ) -> None:

        self.__create_image(unpressed, pressed)
        self.button.itemconfig(self.currentImage, image=self.unpressed)
    
    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def change_click_func(self, new: Callable = do_nothing):
        self.__clickFunc = new

    def change_unclick_func(self, new: Callable = do_nothing):
        self.__unclickFunc = new

    def get_button(self):
        return self.button

    def __create_image(self, unpressed, pressed) -> None:
        self.unpressed = ImageTk.PhotoImage(Image.open(unpressed))
        self.pressed = ImageTk.PhotoImage(Image.open(pressed))
        width, height = self.unpressed.width(), self.unpressed.height()
        self.button.config(self.button, width=width, height=height)

    def __click(self, event) -> None:
        if self.enabled:
            self.button.itemconfig(self.currentImage, image=self.pressed)
            self.__clickFunc()

    def __unclick(self, event) -> None:
        if self.enabled:
            self.button.itemconfig(self.currentImage, image=self.unpressed)
            self.__unclickFunc()

class CombatLog():
    def __init__(
            self,
            root: Tk,
            xPos: int = 0,
            yPos: int = 50,
            colour: str = BGCOLOUR
            ) -> None:
        
        #self.bar = Scrollbar(root, orient='vertical')
        #self.bar.pack(side='right', fill='y')
        
        self.text = Text(root, state='disabled', bg=colour, fg='white', bd=0, highlightthickness=0) # Add ', yscrollcommand=self.bar.set' for scrollbar, not currently functional
        self.text.pack(side='left', expand='True', anchor='nw', fill='both')
        self.text.place(x=xPos, y=yPos, height=PANEL_HEIGHT - xPos, width=PANEL_WIDTH)
        self.text.insert('end', 'meow')
        self.index = 0
        
    def add_text(self, text: str) -> None:
        self.text.config(state='normal')
        self.text.insert('end', f"[{self.index}] {text}")
        self.text.config(state='disabled')
        self.text.see('end')
        self.index += 1

class ActionMenu:
    def __init__(self, x_pos: int, y_pos: int, unit, board) -> None:
        #create a window to fit all three buttons, based on the x and y coordinates
        #get the title of the special ability by calling the unit.special_ability_name() method
        #place the 3 buttons in the window
        #bind the unit.get_targets(), unit.special_abiity(), and board.cancel_action() methods to them
        pass
    