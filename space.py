from constants import TerrainType

class Terrain:
    def __init__(self, space, sprite, move_cost, defense_mod) -> None:
        self.__space = space
        self._sprite = sprite
        self.__move_cost = move_cost
        self.__defense_mod = defense_mod
        
    def get_space(self):
        return self.__space
        
    def get_sprite(self):
        return self._sprite
    
    def get_move_cost(self):
        return self.__move_cost
    
    def get_defense_mod(self):
        return self.__defense_mod
    
class Plains(Terrain):
    def __init__(self, space) -> None:
        sprite = TerrainType.PLAINS
        move_cost = 1
        defense_mod = 0
        super().__init__(space, sprite, move_cost, defense_mod)
        
class Forest(Terrain):
    def __init__(self, space) -> None:
        sprite = TerrainType.FOREST
        move_cost = 1.5
        defense_mod = 1
        super().__init__(space, sprite, move_cost, defense_mod)
        
class Fortress(Terrain):
    def __init__(self, space) -> None:
        sprite = TerrainType.FORTRESS
        move_cost = 1
        defense_mod = 2
        super().__init__(space, sprite, move_cost, defense_mod)
        
class Path(Terrain):
    def __init__(self, space) -> None:
        sprite = None
        move_cost = 0.7
        defense_mod = 0
        super().__init__(space, sprite, move_cost, defense_mod)
        
    def get_sprite(self):
        if self._sprite == None:
            self.set_path_sprite()
        return self._sprite
    
    def set_path_sprite(self):
        space = self.get_space()
        path_string = "path_"
        north_space = space.get_up()
        if north_space != None:
            if north_space.is_path() or north_space.is_fortress():
                path_string += "n"
        east_space = space.get_right()
        if east_space != None:
            if east_space.is_path():
                path_string += "e"
        south_space = space.get_down()
        if south_space != None:
            if south_space.is_path() or south_space.is_fortress():
                path_string += "s"
        west_space = space.get_left()
        if west_space != None:
            if west_space.is_path():
                path_string += "w"
        if path_string == "path_":
            path_string = "path_n"
            print(f"Error: disconnected path object at row: {space.get_row()} col: {space.get_col()}")
        self._sprite = path_string
        

class Space:
    def __init__(
            self,
            row: int,
            col: int,
            ) -> None:
        self.__row = row
        self.__col = col
        self.__terrain = None
        self.__unit = None
        self.__selected = False
        self.__left = None
        self.__up = None
        self.__right = None
        self.__down = None

    def get_unit(self):
        return self.__unit
    
    def assign_unit(self, unit):
        self.__unit = unit

    def get_terrain(self):
        return self.__terrain
    
    def get_terrain_sprite(self):
        if self.__terrain == None:
            return None
        return self.__terrain.get_sprite()
    
    def get_move_cost(self):
        if self.__terrain == None:
            return 1
        return self.__terrain.get_move_cost()
    
    def get_defense_mod(self):
        if self.__terrain == None:
            return 0
        return self.__terrain.get_defense_mod()
    
    def get_unit_sprite(self):
        if self.__unit == None:
            return None
        return self.__unit.get_sprite()
    
    def contains_unit_type(self, unit_type) -> bool:
        if self.__unit != None:
            return self.__unit.is_unit_type(unit_type)
        else:
            return False
    
    def set_terrain(self, terrain: Terrain):
        self.__terrain = terrain
    
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
    
    def set_left(self, space):
        self.__left = space

    def set_up(self, space):
        self.__up = space

    def set_right(self, space):
        self.__right = space

    def set_down(self, space):
        self.__down = space

    def get_left(self):
        return self.__left
    
    def get_up(self):
        return self.__up
    
    def get_right(self):
        return self.__right
    
    def get_down(self):
        return self.__down

    def is_path(self) -> bool:
        if isinstance(self.get_terrain(), Path):
            return True
        return False
    
    def is_fortress(self) -> bool:
        if isinstance(self.get_terrain(), Fortress):
            return True
        return False