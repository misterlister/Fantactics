from tkinter import Tk, LabelFrame, Canvas
from PIL import ImageTk, Image

FONT = 'placeholder'
BGCOLOUR = '#5d4037'
PANEL_WIDTH = 320
PANEL_HEIGHT = 720

class UserInterface():
    def __init__(self, root: Tk):
        self.statsPanel = Panel(root)
        self.statsPanelItems = {'playButton': PlayButton(self.statsPanel.getFrame(), 50, 50)}
        

        self.logPanel = Panel(root, 1280-PANEL_WIDTH, 0)
        
        
class Panel():
    def __init__(self, root: Tk, xPos: int = 0, yPos: int = 0) -> None:
        self.frame = LabelFrame(root, width = PANEL_WIDTH, height = PANEL_HEIGHT, bg=BGCOLOUR, bd=0)
        self.frame.pack_propagate(0)                                                              # Prevent the LabelFrame from shrinking
        self.frame.pack(side = 'left', expand = 'True', anchor='nw', fill='both')
        self.frame.place(x=xPos, y=yPos)

    def getFrame(self):
        return self.frame
    
    def hide(self):
        pass

    def show(self):
        pass

# Base class for buttons with a sprite
class CanvasButton():
    def __init__(self, frame, xPos, yPos) -> None:
        self.button = Canvas(frame, bg=BGCOLOUR, bd=0, highlightthickness=0)
        self.button.pack_propagate(0)
        self.button.pack(expand=1, fill=None)
        self.button.place(x=xPos, y=yPos)
        self.button.bind('<Button-1>', self.click)
        self.button.bind('<ButtonRelease-1>', self.unclick)
       

class PlayButton(CanvasButton):
    def __init__(self, frame, xPos, yPos) -> None:
        super().__init__(frame, xPos, yPos)
        self.assets = self.__load_assets()
        width, height = self.assets['play_unpressed'].width(), self.assets['play_unpressed'].height()
        self.button.config(self.button, width=width, height=height)
        self.play_image = self.button.create_image(0, 0, anchor = 'nw', image = self.assets['play_unpressed'])
        
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
    


    
        
    
