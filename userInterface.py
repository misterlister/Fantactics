from tkinter import Tk, LabelFrame, Canvas, Text, Label, Scrollbar
from PIL import ImageTk, Image
from graphics import WINDOW_WIDTH, WINDOW_HEIGHT

FONT = 'placeholder'
BGCOLOUR = '#5d4037'
BORDER_WIDTH = 2
PANEL_WIDTH = 320
PANEL_HEIGHT = 720 

class UserInterface():
    def __init__(self, root: Tk):
        self.stats = Panel(root)
        self.statsPanel = {
            'friendlyUnitPanel' : StatsPanel(self.stats.getFrame(), height=PANEL_HEIGHT / 3, colour='blue'),
            'enemyUnitPanel' : Panel(self.stats.getFrame(), yPos=PANEL_HEIGHT / 3, height=PANEL_HEIGHT / 3, colour='white'),
            'terrainPanel' : Panel(self.stats.getFrame(), yPos=(PANEL_HEIGHT / 3) * 2, height=PANEL_HEIGHT / 3, colour='black')
        }
        
        self.log = Panel(root, WINDOW_WIDTH-PANEL_WIDTH, 0)
        self.logItems = {
            'text' : CombatLog(self.log.getFrame())
        }

        self.statsPanelsItems = {
            ### Temp
            'playButton' : PlayButton(self.statsPanel['enemyUnitPanel'].getFrame(), 50, 50, textbox=self.log)
            ###
        }

        self.controlBar = Panel(root, PANEL_WIDTH, PANEL_HEIGHT - 64, width=WINDOW_WIDTH - (2 * PANEL_WIDTH))
        
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
    def __init__(self, 
                 root: Tk, 
                 xPos: int = 0, 
                 yPos: int = 0, 
                 width: int = PANEL_WIDTH, 
                 height: int = PANEL_HEIGHT, 
                 colour: str = BGCOLOUR,
                 ) -> None:
        super().__init__(root, xPos, yPos, width, height, colour)

        self.labels = {
            'name' : Label(self.frame, text='Name:'),
            'health' : Label(self.frame, text='Health:'),
            'damage' : Label(self.frame, text='Damage:'),
            'armour' : Label(self.frame, text='Armour:'),
            'movement' : Label(self.frame, text='Movement:')
            
        }
        
        index = 20
        for item in self.labels:
            self.labels[item].pack()
            self.labels[item].place(x=120, y=index)
            index += 20


        #self.labels['name'].place(x=120, y=20)
        #self.labels['health'].place(x=120, y=40)
        #self.labels['damage'].place(x=120, y=60)

    def updateText(self, index, new):
        self.labels[index].config(text=new)

    def update(self):
        pass

        
# Base class for buttons with a sprite
# Child classes should override click() and unclick()
class CanvasButton():
    def __init__(
            self, 
            frame: LabelFrame, 
            xPos: int = 0, 
            yPos: int = 0
            ) -> None:
        
        self.button = Canvas(frame, bg=BGCOLOUR, bd=0, highlightthickness=0) # Create the button object
        self.button.pack_propagate(0) # Prevent the Canvas from shrinking
        self.button.pack(expand=1, fill=None)
        self.button.place(x=xPos, y=yPos)
        self.button.bind('<Button-1>', self.click)
        self.button.bind('<ButtonRelease-1>', self.unclick)

    def click(self, event):
        pass

    def unclick(self, event):
        pass
       
class PlayButton(CanvasButton):
    def __init__(self, frame, xPos, yPos, textbox) -> None:
        super().__init__(frame, xPos, yPos)
        self.assets = self.__load_assets()
        width, height = self.assets['play_unpressed'].width(), self.assets['play_unpressed'].height()
        self.button.config(self.button, width=width, height=height)
        self.play_image = self.button.create_image(0, 0, anchor = 'nw', image = self.assets['play_unpressed'])
        self.textbox = textbox
        self.textboxEnabled = True
        
    def click(self, event):
        print(event)
        self.button.itemconfig(self.play_image, image=self.assets['play_pressed'])
        

    def unclick(self, event):
        print(event)
        self.button.itemconfig(self.play_image, image=self.assets['play_unpressed'])

    def __load_assets(self):
        assets = {}
        assets['play_unpressed'] = ImageTk.PhotoImage(Image.open("Assets/Text/play_unpressed.png"))
        assets['play_pressed'] = ImageTk.PhotoImage(Image.open("Assets/Text/play_pressed.png"))
        return assets
    
class ControlBar(Panel):
    def __init__(
            self,
            
            ) -> None:
        pass

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

    
    
        
    
