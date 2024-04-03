from graphics import Window, Point
from tkinter import Tk, Label
from PIL import ImageTk, Image
from userInterface import UserInterface, do_nothing
from constants import *
from units import Soldier


class GameBoard:
    def __init__(self) -> None:
        
        self.__spaces = [[Space(i, j) for j in range(BOARD_COLS)] for i in range(BOARD_ROWS)]
        self.connect_spaces(self.__spaces)
        self.__selected_space = None # Space currently selected
        self.__selected_unit = None # Unit currently selected
        self.__action_space = None # Location where selected unit will move to take an action
        self.__target_space = None # Target space where the selected unit will act on
        self.__area_of_effect_spaces = [] # Spaces within the area of effect of a targeted action
        self.__valid_moves = None # Spaces where the selected unit can move to
        self.__attack_spaces = None # Spaces the selected unit can attack from the selected action space
        self.__ability_spaces = None # Spaces the selected unit can target with their ability from the selected action space
        self.__guarded_spaces = [] # Spaces which are guarded by soldiers, and cannot be targeted with ranged abilities
        self.__action_confirmed = False # Keeps track of if the current action has been confirmed
        self.__game_state = None # Links to game state object
        
    def link_to_state(self, state):
        self.__game_state = state

    def attack_action(self, unit, space):
        self.move_unit(unit, self.__action_space)
        self.combat(unit, space.get_unit())
        self.end_turn()
        return
    
    def ability_action(self, unit, space):
        self.move_unit(unit, self.__action_space)
        self.activate_ability(unit, space)
        self.end_turn()
        return
                
    def connect_spaces(self, spaces):
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if j-1 >= 0:
                    spaces[i][j].set_left(spaces[i][j-1])
                if i-1 >= 0:
                    spaces[i][j].set_up(spaces[i-1][j])
                if j+1 < BOARD_COLS:
                    spaces[i][j].set_right(spaces[i][j+1])
                if i+1 < BOARD_ROWS:
                    spaces[i][j].set_down(spaces[i+1][j])
        
    def get_space(self, row, col):
        return self.__spaces[row][col]
        
    def place_unit(self, unit, row: int, col: int) -> bool:
        if self.__spaces[row][col].get_unit() != None:
            return False
        self.__spaces[row][col].assign_unit(unit)
        return True

    def get_spaces(self):
        return self.__spaces

    def get_movement_spaces(self, unit, space) -> set:
        range = unit.get_movement()
        if unit.get_move_type() == MoveType.FLY:
            pass_dict = TARGET_ALL
        else:
            pass_dict = TARGET_MOVE
        target_dict = TARGET_MOVE
        action = ActionType.MOVE
        valid_spaces = unit.find_target_spaces(space, range, target_dict, action, pass_dict)
        return valid_spaces
    
    def get_ability_spaces(self, unit, space) -> set:
        if unit.ability_expended():
            self.update_info_panel("This unit's ability cannot be used again")
            return []
        range = unit.get_ability_range()
        if range == 0:
            valid_spaces = [self.__action_space]
        else:
            min_range = unit.get_ability_min_range()
            target_dict = unit.get_ability_targets()
            action = ActionType.ABILITY
            valid_spaces = unit.find_target_spaces(space, range, target_dict, action)
            if min_range > 1:
                invalid_spaces = unit.find_target_spaces(space, min_range-1, target_dict)
                valid_spaces = valid_spaces.difference(invalid_spaces)
            if range > 1:
                self.update_guarded_spaces(valid_spaces, unit)
                valid_spaces = valid_spaces.difference(self.__guarded_spaces)
        return valid_spaces
    
    def get_attack_spaces(self, unit, space) -> set:
        range = 1
        target_dict = TARGET_ENEMIES
        action = ActionType.ATTACK
        valid_spaces = unit.find_target_spaces(space, range, target_dict, action)
        return valid_spaces
    
    def update_guarded_spaces(self, valid_spaces, unit):
        guarded_spaces = set()
        for space in valid_spaces:
            target = space.get_unit()
            if target != None:
                if not target.is_ally(unit):
                    if not target.is_unit_type(Soldier):
                        if target.adjacent_to(Soldier, True):
                            guarded_spaces.add(space)
        self.__guarded_spaces = guarded_spaces

    def move_unit(self, unit, space):
        unit.move(space)

    def set_ability_spaces(self, unit, space):
        try:
            self.__ability_spaces = self.get_ability_spaces(unit, space)
        except Exception as e:
            print(e)
    
    def combat(self, unit, target):
        unit_name = unit.get_name()
        target_name = target.get_name()
        unit_loc = unit.get_space()
        target_loc = target.get_space()

        if target.is_dead(): # If the target is dead, remove them and take their place
            target_loc.assign_unit(None)
            self.move_unit(unit, target_loc)

        else: # Otherwise, they will retaliate
            retaliation_log = target.retaliate(unit)

            if unit.is_dead(): # If the unit died, remove them
                unit_loc.assign_unit(None)
                self.__action_space = None
    
    def activate_ability(self, unit, space):
        unit.special_ability(space.get_unit(), space)

    def end_turn(self):
        self.__game_state.next_turn()

    def move_and_wait(self, unit, space):
        self.ui.controlBar.buttons['attack'].untoggle_keys()
        self.move_unit(unit, space)
        self.end_turn()



class Terrain:
    def __init__(self) -> None:
        pass
    

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
    
    def get_defense_mod(self):
        return 0 # self.__terrain.get_defense_mod()
    
    def get_unit_sprite(self):
        if self.__unit == None:
            return None
        return self.__unit.get_sprite()
    
    def contains_unit_type(self, unit_type) -> bool:
        if self.__unit != None:
            return self.__unit.is_unit_type(unit_type)
        else:
            return False
    
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

