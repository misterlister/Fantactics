from tkinter import Tk, LabelFrame, Canvas, Text, Label, Message, messagebox, Scrollbar
from PIL import ImageTk, Image
from typing import Callable
from constants import (
    ERROR_PRESSED, 
    ERROR_UNPRESSED,
    PANEL_HEIGHT,
    WINDOW_WIDTH,
    PANEL_WIDTH,
    CONTROL_PANEL_HEIGHT,
    BG_COL,
    UI_BG_COLOUR,
    STATS_IMAGE_SIZE,
    EMPTY_SPRITE,
    BORDER_WIDTH,
    FONT,
    DEFAULT_FONT_SIZE,
    SPRITE_BUFFER,
    DamageType,
    ArmourType
    )

# It does nothing
def do_nothing(nothing = None): 
    pass
    
class UserInterface():
    def __init__(self, root: Tk):

        # Create Stats Panel (left side panel)
        self.stats = Panel(root)
        self.statsPanel = { # Stats panel is divided into 3 seperate sub panels
            'friendlyUnitPanel' : StatsPanel(self.stats.getFrame(), height=PANEL_HEIGHT / 3, bgColour='#754239'),
            'enemyUnitPanel' : StatsPanel(self.stats.getFrame(), yPos=PANEL_HEIGHT / 3, height=PANEL_HEIGHT / 3, bgColour='#57312a'),
            'terrainPanel' : TerrainPanel(self.stats.getFrame(), yPos=(PANEL_HEIGHT / 3) * 2, height=PANEL_HEIGHT / 3, bgColour='#4f473b')
        }
        
        ### Create Log Panel (right side panel), multiple panels as for future additions
        self.log = Panel(root, WINDOW_WIDTH-PANEL_WIDTH, 0)
        self.logItems = {
            'text' : CombatLog(self.log.getFrame(), yPos= 50, height=PANEL_HEIGHT - CONTROL_PANEL_HEIGHT - 50)
        }

        ### Top Info bar for displaying text to user
        self.info = InfoPanel(root, PANEL_WIDTH, 0, width=WINDOW_WIDTH - (2 * PANEL_WIDTH), height=25, colour=BG_COL)

        ### Bottom button bar for game controls
        self.controlBar = ControlBar(root, PANEL_WIDTH, PANEL_HEIGHT - CONTROL_PANEL_HEIGHT, width=WINDOW_WIDTH - (2 * PANEL_WIDTH), height=CONTROL_PANEL_HEIGHT)

        #self.end = EndScreen(root, 1)

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
            colour: str = UI_BG_COLOUR,
            bd: int = 0,
            relief: str = 'solid'
            ) -> None:
        
        self.root = root
        self.frame = LabelFrame(root, width = width, height = height, bg=colour, bd=bd, relief=relief)
        self.frame.pack_propagate(0) # Prevent the LabelFrame from shrinking
        self.frame.place(x=xPos, y=yPos)

    def getFrame(self):
        return self.frame
    
    def getRoot(self):
        return self.root
    
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
            bgColour: str = UI_BG_COLOUR,
            bd: int = 0,
            relief: str = 'solid',
            textColour: str = 'white',
            ) -> None:
        super().__init__(root, xPos, yPos, width, height, bgColour, bd, relief)

        ### Create the area for sprite to be displayed on click
        self.spriteCanvas = Canvas(self.frame, width=STATS_IMAGE_SIZE, height=STATS_IMAGE_SIZE, highlightthickness=0, borderwidth=BORDER_WIDTH, relief='solid')
        self.spriteCanvas.pack_propagate(0)
        self.spriteCanvas.place(x=0, y=25)

        self.bgImg = ImageTk.PhotoImage(Image.open("Assets/stats_image_background.png"))
        self.spriteCanvas.create_image(0, 0, anchor ='nw', image=self.bgImg)

        # Empty default sprite for no unit selected
        self.empty = ImageTk.PhotoImage(Image.open(EMPTY_SPRITE))
        self.selectedSprite = self.spriteCanvas.create_image((STATS_IMAGE_SIZE / 2), (STATS_IMAGE_SIZE / 2), anchor = 'center', image=self.empty)

        # Icons to be displayed alongside labels
        self.icons = {
            'class' : ImageTk.PhotoImage(Image.open('Assets/Icons/class.png')),
            'health' : ImageTk.PhotoImage(Image.open('Assets/Icons/health.png')),
            'damage' : ImageTk.PhotoImage(Image.open('Assets/Icons/damage.png')),
            'defense' : ImageTk.PhotoImage(Image.open('Assets/Icons/armour.png')),
            'movement' : ImageTk.PhotoImage(Image.open('Assets/Icons/movement.png')),
        }
        # Label fields for stats to be displayed
        self.labels = {
            'name' : Label(self.frame, text='Name:'),
            'class' : Label(self.frame, text=' ', image=self.icons['class'], compound='right'),
            'health' : Label(self.frame, text='   ', image=self.icons['health'], compound='right'),
            'damage' : Label(self.frame, text=' ', image=self.icons['damage'], compound='right'),
            'defense' : Label(self.frame, text=' ', image=self.icons['defense'], compound='right'),
            'movement' : Label(self.frame, text=' ', image=self.icons['movement'], compound='right'),
            'description' : Message(self.frame, text=' ', width=165)
        }
        
        index = -12
        for item in self.labels:
            self.labels[item].config(bg=bgColour, fg=textColour, font=(FONT, DEFAULT_FONT_SIZE))
            self.labels[item].place(x=width, y=index, anchor = 'ne')
            index += 35

        self.labels['name'].place(x=0, y=0, anchor='nw')
        self.labels['description'].place(x=0, y=STATS_IMAGE_SIZE + 35, anchor='nw')

    # Clear all data from stat display
    def clear(self) -> None:
        self.update_name()
        self.update_class()
        self.update_health()
        self.update_damage()
        self.update_defense()
        self.update_movement()   
        self.update_description()
        self.update_image(self.empty)

    # Update classes to be called during selection of a unit
    def update_name(self, new: str = ' ') -> None: self.labels['name'].config(text= f"Name: {new} ")
        
    def update_class(self, new: str = ' ') -> None: self.labels['class'].config(text= f" {new} ")

    # For "diffType" variable:
    # 0 = damage
    # 1 = healing
    def update_health(self, new: str = ' ', max: str = '', diff: int = 0, diffType: bool = 0) -> None:
        if new != ' ':
            if diff != 0:
                if diffType == 0:
                    self.labels['health'].config(text= f" {new} (-{diff}) / {max}  ")
                else:
                    self.labels['health'].config(text= f" {new} (+{diff}) / {max}  ")
            else:
                self.labels['health'].config(text= f" {new} / {max}  ")
        else:
            self.labels['health'].config(text= f"  ")

    def update_damage(self, new: str = ' ', type: int = 0, diff: int = 0) -> None:
        if type == DamageType.SLASH:
            type = 'Slash'
        elif type == DamageType.PIERCE:
            type = 'Pierce'
        elif type == DamageType.BLUDGEON:
            type = 'Bludgeon'
        elif type == DamageType.MAGIC:
            type = 'Magic'
        else:
            type = ''

        if diff != 0:
            if diff > 0:
                sign = "+"
            else:
                sign = ""
            self.labels['damage'].config(text= f" {new} ({sign}{diff}) {type} ")
        else:
            self.labels['damage'].config(text= f" {new} {type} ")

    def update_defense(self, type: int = 0, diff: int = 0) -> None:
        if type == ArmourType.ROBES:
            type = 'Robes'
        elif type == ArmourType.PADDED:
            type = 'Padded'
        elif type == ArmourType.CHAIN:
            type = 'Chain'
        elif type == ArmourType.PLATE:
            type = 'Plate'
        else:
            type = ''

        if diff != 0:
            if diff > 0:
                sign = "+"
            else:
                sign = ""
            self.labels['defense'].config(text= f" ({sign}{diff}) {type} ")
        else:
            self.labels['defense'].config(text= f" {type} ")

    def update_movement(self, new: str = ' ', type: str = '') -> None:
        self.labels['movement'].config(text= f" {new} {type} ")
    
    def update_description(self, name: str = ' ', new: str = ' ') -> None:
        if new != ' ' and name != ' ':
            self.labels['description'].config(text= f"{name}:\n{new}")
        else:
            self.labels['description'].config(text="")

    def update_image(self, image: ImageTk) -> None:
        self.spriteCanvas.itemconfig(self.selectedSprite, image=image)

class TerrainPanel(Panel):
    def __init__(self,
                root: Tk, 
                xPos: int = 0,
                yPos: int = 0, 
                width: int = PANEL_WIDTH, 
                height: int = PANEL_HEIGHT, 
                bd: int = 0, 
                relief: str = 'solid',
                bgColour: str = UI_BG_COLOUR,
                textColour: str = 'white',
                spriteBgColour: str = '#757eff'
                ) -> None:
        super().__init__(root, xPos, yPos, width, height, bgColour, bd, relief)

        self.spriteCanvas = Canvas(self.frame, width=STATS_IMAGE_SIZE, height=STATS_IMAGE_SIZE, highlightthickness=0, borderwidth=BORDER_WIDTH, relief='solid')
        self.spriteCanvas.place(x=0, y=0)
        self.empty = ImageTk.PhotoImage(Image.open(EMPTY_SPRITE))
        self.bgImg = ImageTk.PhotoImage(Image.open('Assets/terrain_image_background.png'))
        self.selectedSprite = self.spriteCanvas.create_image(0, 0, anchor='nw', image=self.bgImg)
        self.selectedSprite = self.spriteCanvas.create_image(SPRITE_BUFFER*2, SPRITE_BUFFER*2, anchor = 'nw', image=self.empty)

        self.nameLabel = Label(self.frame, text='', bg=bgColour, fg=textColour, font=(FONT, 2 * DEFAULT_FONT_SIZE))
        self.nameLabel.place(x=STATS_IMAGE_SIZE + (6 * BORDER_WIDTH) + 1 , y=0)

        self.descriptionLabel = Message(self.frame, text='', bg=bgColour, fg=textColour, font=(FONT, DEFAULT_FONT_SIZE), width=160)
        self.descriptionLabel.place(x=STATS_IMAGE_SIZE + (5 * BORDER_WIDTH) + 1 , y=40)

        self.icons = {
            'defense' : ImageTk.PhotoImage(Image.open('Assets/Icons/armour.png')),
            'movement' : ImageTk.PhotoImage(Image.open('Assets/Icons/movement.png')),
        }

        self.labels = {
            "defense" : Label(self.frame, text = ' ', image=self.icons['defense'], compound='top'),
            "movement" : Label(self.frame, text = ' ', image=self.icons['movement'], compound='top'),
        }

        index = 30
        for item in self.labels:
            self.labels[item].config(bg=bgColour, fg=textColour, font=(FONT, DEFAULT_FONT_SIZE))
            self.labels[item].place(x=index, y=STATS_IMAGE_SIZE + 10, anchor='n')
            index += 50


    def update_image(self, image: ImageTk):
        self.spriteCanvas.itemconfig(self.selectedSprite, image=image)
    
    def update_name(self, new: str = ""):
        if new != "":
            self.nameLabel.config(text=f"{new}")
        else:
            self.nameLabel.config(text=f"")

    def update_description(self, new: str = ""):
        if new != "":
            self.descriptionLabel.config(text=f"{new}")
        else:
            self.descriptionLabel.config(text=f"")

    def update_defense(self, new: int = 0):
        if new != 0:
            self.labels['defense'].config(text=f"+ {new}")
        else:
            self.labels['defense'].config(text=f" ")

    def update_movement(self, new: int = 0):
        if new != 0:
            self.labels['movement'].config(text=f"{new}")
        else:
            self.labels['movement'].config(text=f" ")
            
    def update_terrain_panel(self, image: ImageTk=None, name: str="", description:str="", defense: int=0, movement: int=0):
        if image == None:
            image = self.empty
        self.update_image(image)
        self.update_name(name)
        self.update_description(description)
        self.update_defense(defense)
        self.update_movement(movement)

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
            colour: str = UI_BG_COLOUR,
            bd: int = 0,
            relief: str = 'solid'
            ) -> None:
        super().__init__(root, xPos, yPos, width, height, colour, bd, relief)

        self.buttons = {
            'attack' : ToggleButton(self.frame, unpressed='Assets/Buttons/red_unpressed.png', pressed='Assets/Buttons/red_pressed.png'),
            'ability' : ToggleButton(self.frame, unpressed='Assets/Buttons/yellow_unpressed.png', pressed='Assets/Buttons/yellow_pressed.png'),
            'confirm' : CanvasButton(self.frame, unpressed='Assets/Buttons/green_unpressed.png', pressed='Assets/Buttons/green_pressed.png'),
            'cancel' : CanvasButton(self.frame, unpressed='Assets/Buttons/grey_unpressed.png', pressed='Assets/Buttons/grey_pressed.png')
        }

        self.__actionToggleKeys = [self.buttons['attack'], self.buttons['ability']]
        self.buttons['attack'].set_key(self.__actionToggleKeys)
        self.buttons['ability'].set_key(self.__actionToggleKeys)

        self.labels = {
            'attack' : Label(self.frame, text='Attack [Z]'),
            'ability' : Label(self.frame, text='Ability [X]'),
            'confirm' : Label(self.frame, text='Confirm [Space]'),
            'cancel' : Label(self.frame, text='Cancel [LShift]')
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

# Display text on top of screen             
class InfoPanel(Panel):
    def __init__(
            self, 
            root: Tk, 
            xPos: int = 0, 
            yPos: int = 0, 
            width: int = PANEL_WIDTH,
            height: int = PANEL_HEIGHT,
            colour: str = UI_BG_COLOUR,
            bd: int = 0,
            relief: str = 'solid'
            ) -> None:
        super().__init__(root, xPos, yPos, width, height, colour, bd, relief)

        self.label = Label(self.frame, text='', justify='center', bg=colour, fg='black', font=(FONT, DEFAULT_FONT_SIZE))
        self.label.place(x=width/2, y=0, anchor='n')
    
    def update(self, new: str):
        self.label.config(text=new)

    def clear(self):
        self.label.config(text='')

# Base class for buttons with a sprite
class CanvasButton():
    def __init__(
            self, 
            frame: LabelFrame, 
            xPos: int = 0, 
            yPos: int = 0,
            bg = UI_BG_COLOUR,
            unpressed: str = ERROR_UNPRESSED,
            pressed: str = ERROR_PRESSED,
            clickFunc: Callable = do_nothing,
            unclickFunc: Callable = do_nothing,
            enabled: bool = True,
            ) -> None:
        
        self.button = Canvas(frame, bg=bg, bd=0, highlightthickness=0, cursor='hand2') # Create the button object
        self.button.pack_propagate(0) # Prevent the Canvas from shrinking
        self.place(xPos, yPos)
        self.bind(self.click, self.unclick)
        self.__create_image(unpressed, pressed)
        self.currentImage = self.button.create_image(0, 0, anchor = 'nw', image=self.unpressed)

        self.clickFunc = clickFunc
        self.unclickFunc = unclickFunc
        self.enabled = enabled

    def place(self, xPos, yPos, anchor: str = 'nw'):
        self.button.place(x=xPos, y=yPos, anchor=anchor)

    def destroy(self):
        self.button.destroy()

    def bind(self, click: Callable = do_nothing, unclick: Callable = do_nothing):
        self.button.bind('<Button-1>', click)
        self.button.bind('<ButtonRelease-1>', unclick)

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

    def change_click_func(self, new: Callable = do_nothing): self.clickFunc = new

    def change_unclick_func(self, new: Callable = do_nothing): self.unclickFunc = new

    def get_button(self): return self.button

    def hide(self): self.button.place_forget()

    def show(self): self.button.place

    def __create_image(self, unpressed, pressed) -> None:
        self.unpressed = ImageTk.PhotoImage(Image.open(unpressed))
        self.pressed = ImageTk.PhotoImage(Image.open(pressed))
        width, height = self.unpressed.width(), self.unpressed.height()
        self.button.config(self.button, width=width, height=height)

    def click(self, event) -> None:
        if self.enabled:
            self.button.itemconfig(self.currentImage, image=self.pressed)
            self.clickFunc()

    def unclick(self, event) -> None:
        if self.enabled:
            self.button.itemconfig(self.currentImage, image=self.unpressed)
            self.unclickFunc()

# Buttons which can be toggled
class ToggleButton(CanvasButton):
    def __init__(self,
                frame: LabelFrame,
                xPos: int = 0,
                yPos: int = 0,
                unpressed: str = ERROR_UNPRESSED, 
                pressed: str = ERROR_PRESSED, 
                clickFunc: Callable = do_nothing, 
                unclickFunc: Callable = do_nothing, 
                enabled: bool = True,
                toggled: bool = False,
                bg = UI_BG_COLOUR,
                disable = True
                ) -> None:
        super().__init__(frame, xPos, yPos, bg, unpressed, pressed, clickFunc, unclickFunc, enabled)
        self.toggled = toggled
        self.disabling = disable

        # Must override parent class else it will behave like parent
        self.bind(self.click, self.unclick)
        self.change_click_func(clickFunc)
        self.change_unclick_func(unclickFunc)
        
    # Check if there are any other buttons toggled in key list and untoggle them
    def untoggle_keys(self):
        for item in self.key:
            try:
                if isinstance(item, ToggleButton):
                    # If item is toggled, untoggle it
                    if item.get_toggle_status() == True:
                        item.untoggle()
                        item.enable()
                else:
                    raise Exception
                
            except Exception as e:
                print(e)

    def set_key(self, key) -> None:
        self.key = key

    def get_toggle_status(self):
        return self.toggled
    
    def toggle(self):
        self.toggled = True
        self.button.itemconfig(self.currentImage, image=self.pressed)
        if self.disabling: self.disable()

    def untoggle(self):
        self.toggled = False
        self.button.itemconfig(self.currentImage, image=self.unpressed)
        self.enable()

    def click(self, event) -> None:
        if self.enabled:
            self.clickFunc()

    def unclick(self, event) -> None:
        if self.enabled:
            if self.disabling: self.untoggle_keys()
            if self.get_toggle_status() == False:
                self.toggle()
                self.unclickFunc()
            else:
                self.untoggle()
                self.unclickFunc()


class CombatLog():
    def __init__(
            self,
            root: Tk,
            xPos: int = 0,
            yPos: int = 0,
            width: int = PANEL_WIDTH,
            height: int = PANEL_HEIGHT,
            colour: str = UI_BG_COLOUR
            ) -> None:
        
        self.text = Text(root, state='disabled', bg=colour, fg='white', bd=0, font=(FONT, DEFAULT_FONT_SIZE), wrap='word') 
        self.text.pack(side='left', expand='True', anchor='nw', fill='both')
        self.text.place(x=xPos, y=yPos, height=height - xPos, width=width)
        #self.text.tag_config("red", foreground='red')
        self.text.tag_config("boldtext", font=("consolas bold", DEFAULT_FONT_SIZE))
        self.text.insert('end', 'meow')
        self.__game_state = None
        self.label = Label(root, text='', bg=UI_BG_COLOUR, fg='white', font=(FONT, DEFAULT_FONT_SIZE))
        self.label.place(x=0, y=0)
        self.map_label = Label(root, text='', bg=UI_BG_COLOUR, fg='white', font=(FONT, DEFAULT_FONT_SIZE))

    def update_label(self) -> None:
        self.label.config(text=f"Turn {self.get_turn()}: Player {self.get_player()}")
        
    def display_map_name(self, map_name) -> None:
        self.map_label.place(x=0, y=25)
        self.map_label.config(text=f"Map: {map_name}")
        
    def add_text(self, text: str) -> None:
        self.text.config(state='normal')
        self.text.insert('end', f"{text}\n")
        self.text.see('end')
        self.text.config(state='disabled')  
        
    def insert_turn_divider(self):
        self.text.config(state='normal')
        self.text.insert('end', f"-----[Turn {self.get_turn()} - Player {self.get_player()}]-----\n")
        self.text.tag_add("boldtext", 'end-2c linestart', 'end-2c lineend')
        self.text.see('end')
        self.text.config(state='disabled')
        
    def insert_endgame_divider(self):
        self.text.config(state='normal')
        self.text.insert('end', f"-----[Endgame]-----\n\n")
        self.text.tag_add("boldtext", 'end-2c linestart', 'end-2c lineend')
        self.text.see('end')
        self.text.config(state='disabled')

    def link_to_state(self, state):
        self.__game_state = state

    def get_turn(self):
        return self.__game_state.get_turn()
    
    def get_player(self):
        return self.__game_state.get_current_player_num()

class EndScreen(Panel):
    def __init__(
            self,
            root: Tk,
            winner, 
            xPos: int = 0, 
            yPos: int = 0, 
            width: int = PANEL_WIDTH, 
            height: int = PANEL_HEIGHT, 
            colour: str = UI_BG_COLOUR, 
            bd: int = 0, 
            bgColour: str = UI_BG_COLOUR,
            textColour: str = 'white',
            relief: str = 'solid'
            ) -> None:
        super().__init__(root, xPos, yPos, width, height, colour, bd, relief)

        self.message = messagebox.showinfo('Game End', f"Player {winner} Wins!")
        # self.winnerLabel = Label(self.frame, text=f"Player {winner} Wins!", bg=bgColour, fg=textColour)
        # self.winnerLabel.place(x=width / 2, y=0, anchor='n')

    def return_to_start(self):
        pass
        




    