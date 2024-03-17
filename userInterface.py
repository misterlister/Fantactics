from tkinter import Tk, LabelFrame, Canvas, Text, Label, Scrollbar
from PIL import ImageTk, Image
from typing import Callable
from constants import *

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
            'text' : CombatLog(self.log.getFrame(), yPos= 50, height=PANEL_HEIGHT - CONTROL_PANEL_HEIGHT - 50)
        }

        self.controlBar = ControlBar(root, PANEL_WIDTH, PANEL_HEIGHT - CONTROL_PANEL_HEIGHT, width=WINDOW_WIDTH - (2 * PANEL_WIDTH), height=CONTROL_PANEL_HEIGHT)
        self.__game_state = None

    def link_to_state(self, state):
        self.__game_state = state
        self.logItems['text'].link_to_state(state)
        
class Panel():
    def __init__(
            self, 
            root: Tk, 
            xPos: int = 0, 
            yPos: int = 0, 
            width: int = PANEL_WIDTH,
            height: int = PANEL_HEIGHT,
            colour: str = BGCOLOUR,
            bd: int = 0,
            relief: str = 'solid'
            ) -> None:
        
        self.frame = LabelFrame(root, width = width, height = height, bg=colour, bd=bd, relief=relief)
        self.frame.pack_propagate(0) # Prevent the LabelFrame from shrinking
        #self.frame.pack(side = 'left', expand = 'True', anchor='nw', fill='both')
        self.frame.place(x=xPos, y=yPos)

    def getFrame(self):
        return self.frame
    
    def clear(self):
        pass
    
class StatsPanel(Panel):
    def __init__(
            self, 
            root: Tk, 
            xPos: int = 0, 
            yPos: int = 0, 
            width: int = PANEL_WIDTH, 
            height: int = PANEL_HEIGHT, 
            bgColour: str = BGCOLOUR,
            bd: int = 0,
            relief: str = 'solid',
            textColour: str = 'white',
            spriteBgColour: str = '#757eff'
            ) -> None:
        super().__init__(root, xPos, yPos, width, height, bgColour, bd, relief)

        ### Create the area for sprite to be displayed on click
        self.spriteCanvas = Canvas(self.frame, width=STATS_IMAGE_SIZE, height=STATS_IMAGE_SIZE, bg=spriteBgColour, highlightthickness=0, borderwidth=BORDER_WIDTH, relief='solid')
        self.spriteCanvas.pack_propagate(0)
        #self.spriteCanvas.pack(expand=1, fill=None)
        self.spriteCanvas.place(x=0, y=25)

        # Empty default sprite for no unit selected
        self.empty = ImageTk.PhotoImage(Image.open(EMPTY_SPRITE))
        self.selectedSprite = self.spriteCanvas.create_image(SPRITE_BUFFER, SPRITE_BUFFER, anchor = 'nw', image=self.empty)

        # Icons to be displayed alongside labels
        self.icons = {
            'health' : ImageTk.PhotoImage(Image.open('Assets/Icons/health.png')),
            'damage' : ImageTk.PhotoImage(Image.open('Assets/Icons/damage.png'))
        }
        # Label fields for stats to be displayed
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
            self.labels[item].config(bg=bgColour, fg=textColour, font=(FONT, DEFAULT_FONT_SIZE))
            #self.labels[item].pack()
            self.labels[item].place(x=STATS_IMAGE_SIZE + (2 * BORDER_WIDTH) + 1, y=index)
            index += 30

        self.labels['name'].place(x=0, y=0)

    # Clear all data from stat display
    def clear(self) -> None:
        self.update_name()
        self.update_class()
        self.update_health()
        self.update_damage()
        self.update_armour()
        self.update_movement()   
        self.update_image(self.empty)

    # Update classes to be called during selection of a unit
    def update_name(self, new: str = '') -> None:
        self.labels['name'].config(text= f"Name: {new}")
        
    def update_class(self, new: str = '') -> None:
        self.labels['class'].config(text= f"Class: {new}")

    def update_health(self, new: str = '', max: int = None) -> None:
        self.labels['health'].config(text= f" {new} / {max}")

    def update_damage(self, new: str = '', type: int = None) -> None:
        self.labels['damage'].config(text= f" {new} {type}")
    
    def update_armour(self, new: str = '', type: int = None) -> None:
        self.labels['armour'].config(text= f"Armour: {new} {type}")

    def update_movement(self, new: str = '', type: int = None) -> None:
        self.labels['movement'].config(text= f"Movement: {new} {type}")
    
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
            colour: str = BGCOLOUR,
            bd: int = 0,
            relief: str = 'solid'
            ) -> None:
        super().__init__(root, xPos, yPos, width, height, colour, bd, relief)

        self.buttons = {
            'red' : CanvasButton(self.frame, toggleable=False, unpressed='Assets/Buttons/red_unpressed.png', pressed='Assets/Buttons/red_pressed.png'),
            'yellow' : CanvasButton(self.frame, toggleable=False, unpressed='Assets/Buttons/yellow_unpressed.png', pressed='Assets/Buttons/yellow_pressed.png'),
            'green' : CanvasButton(self.frame, unpressed='Assets/Buttons/green_unpressed.png', pressed='Assets/Buttons/green_pressed.png'),
            'grey' : CanvasButton(self.frame, unpressed='Assets/Buttons/grey_unpressed.png', pressed='Assets/Buttons/grey_pressed.png')
        }

        self.labels = {
            'red' : Label(self.frame, text='Attack'),
            'yellow' : Label(self.frame, text='Ability'),
            'green' : Label(self.frame, text='Confirm Move'),
            'grey' : Label(self.frame, text='Cancel')
        }

        spacing = 16
        index = 0
        for item in self.buttons:
            self.buttons[item].get_button().place(x=(48 * 3 * index) + (spacing / 2) + (index * spacing), y=8)
            try:
                self.labels[item].config(bg=colour, fg='white', justify='center', font=(FONT, DEFAULT_FONT_SIZE))
                self.labels[item].place(x=(48 * 3 * index) + (spacing / 2) + (index * spacing) + ((48 * 3) / 2), y=56, anchor='n')
            except Exception as e:
                print(e)
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
            toggleable: bool = False
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
        self.toggleable = toggleable
        if self.toggleable:
            self.toggled = False

    def change_image(
            self, 
            unpressed: str = ERROR_UNPRESSED, 
            pressed: str = ERROR_PRESSED
            ) -> None:

        self.__create_image(unpressed, pressed)
        self.button.itemconfig(self.currentImage, image=self.unpressed)
    
    def enable(self):
        self.enabled = True
        self.button.config(cursor='hand2')

    def disable(self):
        self.enabled = False
        self.button.config(cursor='arrow')

    def toggle(self):
        if self.toggled:
            self.toggled = False
            self.button.config(cursor='hand2')
        else:
            self.toggled = True
            self.button.config(cursor='arrow')

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
            if self.toggleable and self.toggled == False:
                self.button.itemconfig(self.currentImage, image=self.pressed)
                self.toggle()
                self.__unclickFunc()
                return None
            elif self.toggleable and self.toggled == True:
                self.button.itemconfig(self.currentImage, image=self.unpressed)
                self.toggle()
                self.__unclickFunc()
                return None
            self.button.itemconfig(self.currentImage, image=self.unpressed)
            self.__unclickFunc()

class CombatLog():
    def __init__(
            self,
            root: Tk,
            xPos: int = 0,
            yPos: int = 0,
            width: int = PANEL_WIDTH,
            height: int = PANEL_HEIGHT,
            colour: str = BGCOLOUR
            ) -> None:
        
        #self.bar = Scrollbar(root, orient='vertical')
        #self.bar.pack(side='right', fill='y')
        
        self.text = Text(root, state='disabled', bg=colour, fg='white', bd=0, font=(FONT, DEFAULT_FONT_SIZE), wrap='word') # Add ', yscrollcommand=self.bar.set' for scrollbar, not currently functional
        self.text.pack(side='left', expand='True', anchor='nw', fill='both')
        self.text.place(x=xPos, y=yPos, height=height - xPos, width=width)
        #self.text.tag_config("red", foreground='red')
        self.text.insert('end', 'meow')
        self.__game_state = None
        self.lastTurn = 0
        self.label = Label(root, text='', bg=BGCOLOUR, fg='white', font=(FONT, DEFAULT_FONT_SIZE))
        self.label.place(x=0, y=0)

    def update_label(self) -> None:
        self.label.config(text=f"Turn {self.get_turn()}: Player {self.get_player()}")
        
    def add_text(self, text: str) -> None:
        self.text.config(state='normal')
        if self.lastTurn is not self.get_turn():
            self.text.insert('end', f"-----[Turn {self.get_turn()}]-----\n")
            #self.text.tag_add("red", 'end-2c linestart', 'end-2c lineend')
        self.text.insert('end', f"{text}\n")
        self.text.see('end')
        self.lastTurn = self.get_turn()
        self.text.config(state='disabled')  

    def link_to_state(self, state):
        self.__game_state = state

    def get_turn(self):
        return self.__game_state.get_turn()
    
    def get_player(self):
        return self.__game_state.get_current_player_num()


    