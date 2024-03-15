from tkinter import Tk, BOTH, Canvas, PhotoImage
from PIL import ImageTk, Image

BG_COL = '#d9d9d9'
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
LINE_WIDTH = 2

class SpriteType:
    ARCHER1 = "Archer1"
    PEASANT1 = "Peasant1"
    SOLDIER1 = "Soldier1"
    SORCERER1 = "Sorcerer1"
    HEALER1 = "Healer1"
    ARCHMAGE1 = "Archmage1"
    ARCHER2 = "Archer2"
    PEASANT2 = "Peasant2"
    SOLDIER2 = "Soldier2"
    SORCERER2 = "Sorcerer2"
    HEALER2 = "Healer2"
    ARCHMAGE2 = "Archmage2"

class Point:
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y

class Window:
    def __init__(self, width_val: int, height_val: int, root: Tk) -> None:
        self.__root = root
        self.__root.title("Fantactics")
        self.__root.geometry(f"{width_val}x{height_val}")
        self.__root.configure(background=BG_COL)
        self.__root.resizable(False, False)
        self.canvas = Canvas(self.__root)
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.configure(background=BG_COL)
        self.sprites = self.__load_sprites()

    def draw_line(self, p1: Point, p2: Point, fill_colour = "black", width: int = LINE_WIDTH) -> None:
        self.canvas.create_line(
            p1.x, 
            p1.y, 
            p2.x, 
            p2.y, 
            fill=fill_colour, 
            width=width
        )
        self.canvas.pack()

    def draw_sprite(self, x: int, y: int, sprite: str) -> None:
        sprite_image = self.sprites[sprite]
        self.canvas.create_image(x, y, anchor='nw', image=sprite_image)

    def get_sprite(self, index):
        return self.sprites[index]

    def __load_sprites(self):
        sprites = {}
        sprites[SpriteType.ARCHER1] = ImageTk.PhotoImage(Image.open("Assets/Units/archer_white.png"))
        sprites[SpriteType.PEASANT1] = ImageTk.PhotoImage(Image.open("Assets/Units/peasant_white.png"))
        sprites[SpriteType.SOLDIER1] = ImageTk.PhotoImage(Image.open("Assets/Units/soldier_white.png"))
        sprites[SpriteType.SORCERER1] = ImageTk.PhotoImage(Image.open("Assets/Units/sorcerer_white.png"))
        sprites[SpriteType.HEALER1] = ImageTk.PhotoImage(Image.open("Assets/Units/healer_white.png"))
        sprites[SpriteType.ARCHMAGE1] = ImageTk.PhotoImage(Image.open("Assets/Units/archmage_white.png"))
        sprites[SpriteType.ARCHER2] = ImageTk.PhotoImage(Image.open("Assets/Units/archer_black.png"))
        sprites[SpriteType.PEASANT2] = ImageTk.PhotoImage(Image.open("Assets/Units/peasant_black.png"))
        sprites[SpriteType.SOLDIER2] = ImageTk.PhotoImage(Image.open("Assets/Units/soldier_black.png"))
        sprites[SpriteType.SORCERER2] = ImageTk.PhotoImage(Image.open("Assets/Units/sorcerer_black.png"))
        sprites[SpriteType.HEALER2] = ImageTk.PhotoImage(Image.open("Assets/Units/healer_black.png"))
        sprites[SpriteType.ARCHMAGE2] = ImageTk.PhotoImage(Image.open("Assets/Units/archmage_black.png"))
        return sprites
    