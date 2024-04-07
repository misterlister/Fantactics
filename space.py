from constants import TerrainType

class Terrain:
    def __init__(self, space, sprite, move_cost, defense_mod, name, description) -> None:
        self.__space = space
        self._sprite = sprite
        self.__move_cost = move_cost
        self.__defense_mod = defense_mod
        self.__name = name
        self.__description = description
        
    def get_space(self):
        return self.__space
        
    def get_sprite(self):
        return self._sprite
    
    def get_move_cost(self):
        return self.__move_cost
    
    def get_defense_mod(self):
        return self.__defense_mod
    
    def get_name(self):
        return self.__name
    
    def get_description(self):
        return self.__description
    
class Plains(Terrain):
    def __init__(self, space) -> None:
        sprite = TerrainType.PLAINS
        move_cost = 1
        defense_mod = 0
        name = "Plains"
        description = "A basic terrain that provides no bonuses or penalties"
        super().__init__(space, sprite, move_cost, defense_mod, name, description)
        
class Forest(Terrain):
    def __init__(self, space) -> None:
        sprite = None
        move_cost = 1.5
        defense_mod = 1
        name = "Forest"
        description = "Provides cover at the cost of mobility, particularly for mounted units"
        super().__init__(space, sprite, move_cost, defense_mod, name, description)
        
    def get_sprite(self):
        if self._sprite == None:
            self.set_forest_sprite()
        return self._sprite
    
    def set_forest_sprite(self):
        space = self.get_space()
        forest_string = "forest_"
        north_space = space.get_up()
        if north_space != None:
            if north_space.is_forest():
                forest_string += "n"
        east_space = space.get_right()
        if east_space != None:
            if east_space.is_forest():
                forest_string += "e"
        south_space = space.get_down()
        if south_space != None:
            if south_space.is_forest():
                forest_string += "s"
        west_space = space.get_left()
        if west_space != None:
            if west_space.is_forest():
                forest_string += "w"
        if forest_string == "forest_":
            forest_string = "forest"
        self._sprite = forest_string
        
class Fortress(Terrain):
    def __init__(self, space) -> None:
        sprite = TerrainType.FORTRESS
        move_cost = 1
        defense_mod = 2
        name = "Fortress"
        description = "Provides a substantial defensive bonus, with no cost to mobility"
        super().__init__(space, sprite, move_cost, defense_mod, name, description)
        
class Path(Terrain):
    def __init__(self, space) -> None:
        sprite = None
        move_cost = 0.7
        defense_mod = 0
        name = "Path"
        description = "Provides additional mobility when traveled upon"
        super().__init__(space, sprite, move_cost, defense_mod, name, description)
        
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

    def is_forest(self) -> bool:
        if isinstance(self.get_terrain(), Forest):
            return True
        return False
    
    def is_fortress(self) -> bool:
        if isinstance(self.get_terrain(), Fortress):
            return True
        return False