from tkinter import Tk, BOTH, Canvas
from PIL import ImageTk, Image
from constants import (
    BG_COL,
    LINE_WIDTH,
    SpriteType,
    TerrainType
)

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

    def draw_line(self, p1: Point, p2: Point, fill_colour = "grey", width: int = LINE_WIDTH) -> None:
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
        
        ### Tag the created image so it can be deleted later.
        self.canvas.create_image(x, y, anchor='nw', image=sprite_image, tags=('temp'))

    def get_sprite(self, index):
        return self.sprites[index]

    def __load_sprites(self):
        sprites = {}
        sprites[SpriteType.ARCHER1] = ImageTk.PhotoImage(Image.open("Assets/Units/White/archer_white.png"))
        sprites[SpriteType.PEASANT1] = ImageTk.PhotoImage(Image.open("Assets/Units/White/peasant_white.png"))
        sprites[SpriteType.SOLDIER1] = ImageTk.PhotoImage(Image.open("Assets/Units/White/soldier_white.png"))
        sprites[SpriteType.SORCERER1] = ImageTk.PhotoImage(Image.open("Assets/Units/White/sorcerer_white.png"))
        sprites[SpriteType.CAVALRY1] = ImageTk.PhotoImage(Image.open("Assets/Units/White/cavalry_white.png"))
        sprites[SpriteType.HEALER1] = ImageTk.PhotoImage(Image.open("Assets/Units/White/healer_white.png"))
        sprites[SpriteType.ARCHMAGE1] = ImageTk.PhotoImage(Image.open("Assets/Units/White/archmage_white.png"))
        sprites[SpriteType.GENERAL1] = ImageTk.PhotoImage(Image.open("Assets/Units/White/general_white.png"))
        
        sprites[SpriteType.ARCHER2] = ImageTk.PhotoImage(Image.open("Assets/Units/Black/archer_black.png"))
        sprites[SpriteType.PEASANT2] = ImageTk.PhotoImage(Image.open("Assets/Units/Black/peasant_black.png"))
        sprites[SpriteType.SOLDIER2] = ImageTk.PhotoImage(Image.open("Assets/Units/Black/soldier_black.png"))
        sprites[SpriteType.SORCERER2] = ImageTk.PhotoImage(Image.open("Assets/Units/Black/sorcerer_black.png"))
        sprites[SpriteType.CAVALRY2] = ImageTk.PhotoImage(Image.open("Assets/Units/Black/cavalry_black.png"))
        sprites[SpriteType.HEALER2] = ImageTk.PhotoImage(Image.open("Assets/Units/Black//healer_black.png"))
        sprites[SpriteType.ARCHMAGE2] = ImageTk.PhotoImage(Image.open("Assets/Units/Black/archmage_black.png"))
        sprites[SpriteType.GENERAL2] = ImageTk.PhotoImage(Image.open("Assets/Units/Black/general_black.png"))
        
        sprites[TerrainType.PLAINS] = ImageTk.PhotoImage(Image.open("Assets/Terrain/plains.png"))
        sprites[TerrainType.FOREST] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest.png"))
        sprites[TerrainType.FORTRESS] = ImageTk.PhotoImage(Image.open("Assets/Terrain/fortress.png"))
        sprites[TerrainType.FORTRESS_N] = ImageTk.PhotoImage(Image.open("Assets/Terrain/fortress_n.png"))
        sprites[TerrainType.PATH_E] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_e.png"))
        sprites[TerrainType.PATH_ES] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_es.png"))
        sprites[TerrainType.PATH_ESW] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_esw.png"))
        sprites[TerrainType.PATH_EW] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_ew.png"))
        sprites[TerrainType.PATH_N] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_n.png"))
        sprites[TerrainType.PATH_NE] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_ne.png"))
        sprites[TerrainType.PATH_NES] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_nes.png"))
        sprites[TerrainType.PATH_NESW] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_nesw.png"))
        sprites[TerrainType.PATH_NEW] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_new.png"))
        sprites[TerrainType.PATH_NS] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_ns.png"))
        sprites[TerrainType.PATH_NSW] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_nsw.png"))
        sprites[TerrainType.PATH_NW] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_nw.png"))
        sprites[TerrainType.PATH_S] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_s.png"))
        sprites[TerrainType.PATH_SW] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_sw.png"))
        sprites[TerrainType.PATH_W] = ImageTk.PhotoImage(Image.open("Assets/Terrain/path_w.png"))
        
        sprites[TerrainType.FOREST_E] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_e.png"))
        sprites[TerrainType.FOREST_ES] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_es.png"))
        sprites[TerrainType.FOREST_ESW] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_esw.png"))
        sprites[TerrainType.FOREST_EW] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_ew.png"))
        sprites[TerrainType.FOREST_N] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_n.png"))
        sprites[TerrainType.FOREST_NE] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_ne.png"))
        sprites[TerrainType.FOREST_NES] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_nes.png"))
        sprites[TerrainType.FOREST_NESW] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_nesw.png"))
        sprites[TerrainType.FOREST_NEW] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_new.png"))
        sprites[TerrainType.FOREST_NS] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_ns.png"))
        sprites[TerrainType.FOREST_NSW] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_nsw.png"))
        sprites[TerrainType.FOREST_NW] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_nw.png"))
        sprites[TerrainType.FOREST_S] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_s.png"))
        sprites[TerrainType.FOREST_SW] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_sw.png"))
        sprites[TerrainType.FOREST_W] = ImageTk.PhotoImage(Image.open("Assets/Terrain/forest_w.png"))
        
        return sprites
    
