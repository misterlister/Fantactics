from tkinter import Tk, LabelFrame, Canvas, Text, Label, Scrollbar
from PIL import ImageTk, Image
from graphics import WINDOW_WIDTH, WINDOW_HEIGHT

SPRITE_BUFFER = 8
STATS_IMAGE_SIZE = (2 * 64) + SPRITE_BUFFER
ERROR_UNPRESSED = "Assets/Text/error_unpressed.png"
ERROR_PRESSED = "Assets/Text/error_pressed.png"
EMPTY_SPRITE = "Assets/Text/empty.png"
FONT = 'placeholder'
BGCOLOUR = '#5d4037'
BORDER_WIDTH = 4
PANEL_WIDTH = 320
PANEL_HEIGHT = 720 

# It does nothing
def do_nothing(): 
    pass
    
class UserInterface():
    def __init__(self, root: Tk):

        # Create Stats Panel (left side panel)
        self.stats = Panel(root)
        self.statsPanel = { # Stats panel is divided into 3 seperate subPanels
            'friendlyUnitPanel' : StatsPanel(self.stats.getFrame(), height=PANEL_HEIGHT / 3, colour='blue'),
            'enemyUnitPanel' : Panel(self.stats.getFrame(), yPos=PANEL_HEIGHT / 3, height=PANEL_HEIGHT / 3, colour='white'),
            'terrainPanel' : Panel(self.stats.getFrame(), yPos=(PANEL_HEIGHT / 3) * 2, height=PANEL_HEIGHT / 3, colour='black')
        }
        
        ### Create Log Panel (right side panel)
        self.log = Panel(root, WINDOW_WIDTH-PANEL_WIDTH, 0)
        self.logItems = {
            'text' : CombatLog(self.log.getFrame())
        }

        self.statsPanelsItems = {
            ### Temp
            'playButton' : CanvasButton(self.statsPanel['enemyUnitPanel'].getFrame(), 50, 50)
            ###
        }

        self.controlBar = ControlBar(root, PANEL_WIDTH, PANEL_HEIGHT - 80, width=WINDOW_WIDTH - (2 * PANEL_WIDTH))
        
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
            colour: str = BGCOLOUR,
            ) -> None:
        super().__init__(root, xPos, yPos, width, height, colour)

        ### Create the area for sprite to be displayed on click
        self.spriteCanvas = Canvas(self.frame, width=STATS_IMAGE_SIZE, height=STATS_IMAGE_SIZE, bg='#757eff', highlightthickness=0, borderwidth=BORDER_WIDTH, relief='solid')
        self.spriteCanvas.pack_propagate(0)
        self.spriteCanvas.pack(expand=1, fill=None)
        self.spriteCanvas.place(x=0, y=20)

        # Empty default sprite for no unit selected
        self.empty = ImageTk.PhotoImage(Image.open(EMPTY_SPRITE))
        self.selectedSprite = self.spriteCanvas.create_image(SPRITE_BUFFER, SPRITE_BUFFER, anchor = 'nw', image=self.empty)

        # Label fields for stats to be displayed
        self.labels = {
            'name' : Label(self.frame, text='Name:'),
            'class' : Label(self.frame, text='Class:'),
            'health' : Label(self.frame, text='Health:'),
            'damage' : Label(self.frame, text='Damage:'),
            'armour' : Label(self.frame, text='Armour:'),
            'movement' : Label(self.frame, text='Movement:')
        }
        
        index = 20
        for item in self.labels:
            self.labels[item].pack()
            self.labels[item].place(x=STATS_IMAGE_SIZE + (2 * BORDER_WIDTH) + 1, y=index)
            index += 20

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
        self.labels['health'].config(text= f"Health: {new}")

    def update_damage(self, new: str = '') -> None:
        self.labels['damage'].config(text= f"Damage: {new}")
    
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
        
# Base class for buttons with a sprite
class CanvasButton():
    def __init__(
            self, 
            frame: LabelFrame, 
            xPos: int = 0, 
            yPos: int = 0,
            unpressed: str = ERROR_UNPRESSED,
            pressed: str = ERROR_PRESSED,
            clickFunc = do_nothing,
            unclickFunc = do_nothing,
            enabled: bool = True,
            ) -> None:
        
        self.button = Canvas(frame, bg=BGCOLOUR, bd=0, highlightthickness=0) # Create the button object
        self.button.pack_propagate(0) # Prevent the Canvas from shrinking
        self.button.pack(expand=1, fill=None)
        self.button.place(x=xPos, y=yPos)
        
        self.__create_image(unpressed, pressed)
        self.currentImage = self.button.create_image(0, 0, anchor = 'nw', image=self.unpressed)

        self.__clickFunc = clickFunc
        self.__unclickFunc = unclickFunc
        self.button.bind('<Button-1>', self.__click)
        self.button.bind('<ButtonRelease-1>', self.__unclick)

    def change_image(
            self, 
            unpressed: str = ERROR_UNPRESSED, 
            pressed: str = ERROR_PRESSED
            ) -> None:

        self.__create_image(unpressed, pressed)
        self.button.itemconfig(self.currentImage, image=self.unpressed)

    def __create_image(self, unpressed, pressed) -> None:
        self.unpressed = ImageTk.PhotoImage(Image.open(unpressed))
        self.pressed = ImageTk.PhotoImage(Image.open(pressed))
        width, height = self.unpressed.width(), self.unpressed.height()
        self.button.config(self.button, width=width, height=height)

    def change_click_func(self):
        pass

    def change_unclick_func(self):
        pass

    def __click(self, event) -> None:
        self.button.itemconfig(self.currentImage, image=self.pressed)
        self.__clickFunc()

    def __unclick(self, event) -> None:
        self.button.itemconfig(self.currentImage, image=self.unpressed)
        self.__unclickFunc()

class CombatLog():
    def __init__(
            self,
            root: Tk,
            xPos: int = 0,
            yPos: int = 50,
            ) -> None:
        
        #self.bar = Scrollbar(root, orient='vertical')
        #self.bar.pack(side='right', fill='y')
        
        self.text = Text(root, state='disabled', bg=BGCOLOUR, fg='white', bd=0, highlightthickness=0) # Add ', yscrollcommand=self.bar.set' for scrollbar, not currently functional
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
    