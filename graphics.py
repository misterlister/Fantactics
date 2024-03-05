from tkinter import Tk, BOTH, Canvas, PhotoImage
from PIL import ImageTk, Image

bg_col = '#d9d9d9'
window_width = 1280
window_height = 720

class SpriteType:
    ARCHER = "Archer"
    PEASANT = "Peasant"
    SOLDIER = "Soldier"
    SORCERER = "Sorcerer"

class Point:
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y

class Window:
    def __init__(self, width_val: int, height_val: int, root: Tk) -> None:
        self.__root = root
        self.__root.title("Fantactics")
        self.__root.geometry(f"{width_val}x{height_val}")
        self.__root.configure(background=bg_col)
        self.canvas = Canvas(self.__root)
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.configure(background=bg_col)
        self.sprites = self.__load_sprites()

    def draw_line(self, p1: Point, p2: Point, fill_colour = "black", width: int = 2) -> None:
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

    def __load_sprites(self):
        sprites = {}
        sprites[SpriteType.ARCHER] = ImageTk.PhotoImage(Image.open("Assets/Units/archer.png"))
        sprites[SpriteType.PEASANT] = ImageTk.PhotoImage(Image.open("Assets/Units/peasant.png"))
        sprites[SpriteType.SOLDIER] = ImageTk.PhotoImage(Image.open("Assets/Units/soldier.png"))
        sprites[SpriteType.SORCERER] = ImageTk.PhotoImage(Image.open("Assets/Units/sorcerer.png"))
        return sprites
    