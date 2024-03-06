from tkinter import Tk, LabelFrame, Canvas
from graphics import Window
from PIL import ImageTk, Image

FONT = 'placeholder'
BGCOLOUR = '#5d4037'

class UserInterface():
    def __init__(
            self, 
            window: Window,
            root: Tk) -> None:
        
        self.__window = window
        self.__root = root
        self.font = FONT

class ControlPanel(UserInterface):
    def __init__(self, window: Window, root: Tk) -> None:
        
        self.__frame = LabelFrame(root, width = 320, height = 720, bg=BGCOLOUR)
        self.__frame.pack_propagate(0) # Prevent the LabelFrame from shrinking
        self.__frame.pack(side = 'left', expand = 'True', anchor='nw', fill='both')
        self.__frame.place(x=1280-320, y=0)
        self.assets = self.__load_assets()
        self.play_button()

    # TEMP
    def play_button(self):
        width, height = self.assets['play_unpressed'].width(), self.assets['play_unpressed'].height()
        self.playButton = Canvas(self.__frame, width=width, height=height, bg=BGCOLOUR, bd=0, highlightthickness=0)
        self.playButton.pack_propagate(0)
        self.playButton.pack(expand=1, fill=None)
        self.playButton.bind('<Button-1>', self.click)
        self.playButton.bind('<ButtonRelease-1>', self.unclick)

        self.play_image = self.playButton.create_image(0, 0, anchor = 'nw', image = self.assets['play_unpressed'])

    # TEMP
    def click(self, event):
        print(event)
        self.playButton.itemconfig(self.play_image, image=self.assets['play_pressed'])

    # TEMP
    def unclick(self, event):
        print(event)
        self.playButton.itemconfig(self.play_image, image=self.assets['play_unpressed'])


    def __load_assets(self):
        assets = {}
        assets['play_unpressed'] = ImageTk.PhotoImage(Image.open("Assets/Text/play_unpressed.png"))
        assets['play_pressed'] = ImageTk.PhotoImage(Image.open("Assets/Text/play_pressed.png"))

        return assets

    def show(self):
        pass

    def hide(self):
        self.__frame.pack_forget()
        
    
