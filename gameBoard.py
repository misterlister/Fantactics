from graphics import Window, Point, WINDOW_HEIGHT, WINDOW_WIDTH, BG_COL
from tkinter import Tk

SPRITE_BUFFER = 8
DEFAULT_SQUARE_SIZE = 64 + SPRITE_BUFFER
SELECTION_BUFFER = 4
SELECTION_SQUARE = DEFAULT_SQUARE_SIZE - SELECTION_BUFFER
DEFAULT_BOARD_ROWS = 8
DEFAULT_BOARD_COLS = 8
BOARD_WIDTH = DEFAULT_SQUARE_SIZE * DEFAULT_BOARD_COLS
BOARD_HEIGHT = DEFAULT_SQUARE_SIZE * DEFAULT_BOARD_ROWS
DEFAULT_X_POS = (WINDOW_WIDTH - BOARD_WIDTH) // 2
DEFAULT_Y_POS = (WINDOW_HEIGHT - BOARD_HEIGHT) // 2


class GameBoard:
    def __init__(
            self,
            window: Window,
            root: Tk,
            x_start: int = DEFAULT_X_POS,
            y_start: int = DEFAULT_Y_POS,
            num_rows: int = DEFAULT_BOARD_ROWS,
            num_cols: int = DEFAULT_BOARD_COLS,
            square_size: int = DEFAULT_SQUARE_SIZE
                 ) -> None:
        self.window = window
        self.root = root
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_start + (num_cols * square_size) 
        self.y_end = y_start + (num_rows * square_size)
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.square_size = square_size
        self.__spaces = [[Space(i, j) for j in range(self.__num_cols)] for i in range(self.__num_rows)]
        self.draw_board()
        self.window.canvas.bind('<Button-1>', self.click)
        self.selected_space = None
        self.selected_unit = None

    def get_num_rows(self):
        return self.__num_rows

    def get_num_cols(self):
        return self.__num_cols
    
    def draw_board(self) -> None:
        for i in range (self.__num_rows + 1):
            y_position = (self.y_start + i * self.square_size)
            p1 = Point(self.x_start, y_position)
            p2 = Point(self.x_end, y_position)
            self.window.draw_line(p1, p2)

        for j in range (self.__num_cols + 1):
            x_position = (self.x_start + j * self.square_size)
            p1 = Point(x_position, self.y_start)
            p2 = Point(x_position, self.y_end)
            self.window.draw_line(p1, p2)

    def click(self, event):
        if event.x > self.x_start and event.x < self.x_end:
            if event.y > self.y_start and event.y < self.y_end:
                row = (event.y-self.y_start) // self.square_size
                col = (event.x-self.x_start) // self.square_size
                contents = self.check_square(row, col)
                print(f"Clicked square {row},{col}. Contents: {contents}")
                new_space = self.__spaces[row][col]
                if self.selected_unit is None: # No unit is currently selected
                    if self.selected_space is not None:
                        if self.selected_space == new_space:
                            self.deselect_space()
                            return
                        self.deselect_space()
                    self.select_space(row, col)
                    return
                else: # A unit is currently selected
                    if self.selected_space == new_space:
                        self.selected_unit.choose_action()
                    else:
                        if new_space.contains() is not None: # Another unit is already here
                            print("Can't Move Here! Space Occupied!")
                        else:  # The space is free
                            self.move_unit(self.selected_unit, new_space)
                    self.deselect_space()
                    return
                
        print("Clicked Outside Grid")

    def outline_space(self, row: int, col: int, colour: str) -> None:
        x1 = self.x_start + (col * (self.square_size)) + SELECTION_BUFFER
        y1 = self.y_start + (row * (self.square_size)) + SELECTION_BUFFER
        x2 = self.x_start + ((col+1) * (self.square_size)) - SELECTION_BUFFER
        y2 = self.y_start + ((row+1) * (self.square_size)) - SELECTION_BUFFER
        self.window.canvas.create_rectangle(x1, y1, x2, y2, width=SPRITE_BUFFER/2, outline=colour)

    def check_square(self, row: int, col: int):
        if row > self.__num_rows or col > self.__num_cols:
            return "Outside Grid"
        else:
            return self.__spaces[row][col].contains()
        
    def get_space(self, row, col):
        return self.__spaces[row][col]
        
    def place_unit(self, unit, row: int, col: int) -> bool:
        if self.__spaces[row][col].contains() != None:
            return False
        self.__spaces[row][col].assign_unit(unit)
        return True
    
    def draw_space(self, space) -> None:
        col = space.get_col()
        row = space.get_row()
        x = self.x_start + SPRITE_BUFFER/2 + (col * self.square_size)
        y = self.y_start + SPRITE_BUFFER/2 + (row * self.square_size)
        #terrain = self.__spaces[i][j].get_terrain()
        #terrain_sprite = terrain.get_sprite()
        #self.window.draw_sprite(x, y, terrain_sprite)

        ###
        self.erase(row, col)
        ###

        unit = space.contains()
        if unit is not None:
            unit_sprite = unit.get_sprite()
            self.window.draw_sprite(x, y, unit_sprite)
        if space.is_selected():
            self.outline_space(row, col, 'blue')

    def draw_sprites(self):
        for i in range(self.__num_rows):
            for j in range(self.__num_cols):
                self.draw_space(self.__spaces[i][j])


###### TEMPORARY
    def erase(self, row, col):
        x1 = self.x_start + (col * (self.square_size))
        y1 = self.y_start + (row * (self.square_size))
        x2 = self.x_start + ((col+1) * (self.square_size))
        y2 = self.y_start + ((row+1) * (self.square_size))
        self.window.canvas.create_rectangle(x1, y1, x2, y2, fill=BG_COL, outline = 'black', width=2)
######

    def movement_spaces(i, j, range):
        valid_spaces = set()
        pass

    def select_space(self, row: int, col: int) -> None:
        new_space = self.__spaces[row][col]
        new_space.select()
        self.selected_space = new_space
        self.selected_unit = new_space.contains()
        self.draw_space(new_space)

    def deselect_space(self) -> None:
        space = self.selected_space
        if space is not None:
            space.deselect()
            self.selected_space = None
            self.selected_unit = None
            self.draw_space(space)

    def move_unit(self, unit, space):
        old_space = unit.get_location()
        try:  
            unit.move(space)
            self.draw_space(old_space)
            self.draw_space(space)
        except Exception as e:
            print(e)



class Terrain:
    def __init__(self) -> None:
        pass
    

class Space:
    def __init__(
            self,
            row: int,
            col: int,
            terrain = None,
            unit = None,
            ) -> None:
        self.__row = row
        self.__col = col
        self.__terrain = terrain
        self.__unit = unit
        self.__selected = False

    def contains(self):
        return self.__unit
    
    def assign_unit(self, unit):
        self.__unit = unit

    def get_terrain(self):
        return self.__terrain
    
    def get_unit_sprite(self):
        if self.__unit == None:
            return None
        return self.__unit.get_sprite()
    
    def get_terrain_sprite(self):
        pass
    
    def get_row(self):
        return self.__row
    
    def get_col(self):
        return self.__col
    
    def select(self):
        self.__selected = True

    def deselect(self):
        self.__selected = False

    def is_selected(self):
        return self.__selected

