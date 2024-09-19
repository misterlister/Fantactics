from units import (
    Unit,
    Peasant,
    )

from time import sleep
import random

from space import Space

from constants import (
    CPU_DELAY,
    SELECT_COL,
    ACTION_COL,
    ATTACK_COL,
    CPU_Persona
)

class Player:
    def __init__(self, team: str) -> None:
        self.__units: list[Unit] = [] # List of all the player's units
        self.__effected_units: Unit = [] # List of this player's units who have time-based effects on them
        self.__game_state = None # Reference to the GameState object
        self.__turn: bool = False # Is it this player's turn?
        self.__extra_turns: int = 0 # Number of extra turns a player has
        self.__team: str = team # Colour name of the player's team
        
    def get_state(self):
        return self.__game_state
    
    def get_team_colour(self):
        return self.__team
    
    def get_unit_list(self):
        return self.__units

    def assign_units(self, unit_list: list):
        for unit in unit_list:
            self.assign_unit(unit)
            
    def assign_unit(self, unit: Unit):
        self.__units.append(unit)
        unit.set_player(self)
        
    def remove_unit(self, unit: Unit):
        self.__units.remove(unit)
            
    def add_effected_unit(self, unit: Unit):
        self.__effected_units.append(unit)

    def join_game(self, game):
        self.__game_state = game

    def start_turn(self):
        self.__turn = True
        
    def end_turn(self):
        self.__turn = False

    def is_current_turn(self):
        return self.__turn

    def has_extra_turn(self):
        if self.__extra_turns > 0:
            return True
        return False
    
    def get_extra_turns(self, turns: int):
        self.__extra_turns += turns
    
    def use_extra_turn(self):
        if self.__extra_turns > 0:
            self.__extra_turns -= 1
            
    def advance_timed_effects(self):
        if len(self.__effected_units) > 0:
            self.end_bravery()
            self.ability_disable_timer()
        
    def end_bravery(self):
        for unit in self.__effected_units:
            if isinstance(unit, Peasant):
                if unit.is_brave():
                    unit.end_brave()
                    self.__effected_units.remove(unit)
                    
    def ability_disable_timer(self):
        for unit in self.__effected_units:
            if unit.ability_disabled():
                unit.decrement_disabled_counter()
                if not unit.ability_disabled():
                    self.__effected_units.remove(unit)
                    
    def surrender(self):
        self.__game_state.team_surrender(self)
        
        
class CPU_Player(Player):
    def __init__(self, team: str) -> None:
        super().__init__(team)
        self.__attacking_units: dict[Unit, dict[Space, list[Unit]]] = {}
        self.__movable_units: dict[Unit, list[Space]] = {}
        self.__persona: str = self.set_persona()
    
    def take_turn(self) -> None:
        print("Choosing Action")
        self.choose_action()
        
    def choose_action(self):
        sleep(CPU_DELAY)
        self.get_attacking_units()
        # If there are no targets to attack, move a unit instead
        if len(self.__attacking_units) == 0:
            self.get_movable_units()
            unit, space = self.choose_move_target()
            self.move_unit(unit, space)
            return
        
        unit = self.choose_attacker()
        target, space = self.choose_attack_target(unit)
        self.attack_action(unit, target, space)
        
    def get_attacking_units(self):
        self.__attacking_units = {}
        for unit in self.get_unit_list():
            spaces = self.get_state().board.get_movement_spaces(unit, unit.get_space())
            attackable_spaces = {} # Temporary dictionary to hold valid attackable spaces
            
            for space in spaces:
                targets = self.get_state().board.get_attack_spaces(unit, space)
                
                if len(targets) > 0: # Only add spaces that have valid attack targets
                    attackable_spaces[space] = targets
                    
            if len(attackable_spaces) > 0: # Only add units that have at least one target
                self.__attacking_units[unit] = attackable_spaces
            
    def get_movable_units(self):
        self.__movable_units = {}
        for unit in self.get_unit_list():
            current_space = unit.get_space()
            spaces = self.get_state().board.get_movement_spaces(unit, unit.get_space())
            if current_space in spaces: # Remove the unit's current space from movement options
                spaces.remove(current_space)
            if len(spaces) > 0: # Only add this unit if it has at least one space to move to
                self.__movable_units[unit] = spaces
    
    def ability_action(self):
        pass
    
    def choose_move_target(self):
        unit = random.choice(list(self.__movable_units.keys()))
        space = random.choice(list(self.__movable_units[unit]))
        return unit, space
    
    def move_unit(self, unit: Unit, space: Space):
        self.select_space(unit.get_space(), SELECT_COL)
        #sleep(CPU_DELAY)
        self.select_space(space, ACTION_COL)
        #sleep(CPU_DELAY)
        self.get_state().board.move_unit(unit, space)
        
    def choose_attacker(self):
        unit = random.choice(list(self.__attacking_units.keys()))
        return unit
        
    def choose_attack_target(self, unit: Unit):
        target_options = []

        # Collect all attackable targets from all spaces
        for space, enemies in self.__attacking_units[unit].items():
            for enemy in enemies:
                target_options.append((enemy, space))  # Store the enemy and the space
        
        # Randomly select a target from the list of options
        if target_options:
            chosen_enemy, chosen_space = random.choice(target_options)
            return chosen_enemy, chosen_space
        else:
            return None, None  # No valid targets
        
    def attack_action(self, unit: Unit, target: Space, move_space: Space):
        self.select_space(unit.get_space(), SELECT_COL)
        #sleep(CPU_DELAY)
        self.select_space(move_space, ACTION_COL)
        #sleep(CPU_DELAY)
        self.select_space(target, ATTACK_COL)
        #sleep(CPU_DELAY)
        self.get_state().board.attack_action(unit, target, move_space)
        
    def select_space(self, space: Space, colour: str):
        if colour == ATTACK_COL or colour == ACTION_COL or colour == SELECT_COL:
            self.get_state().board.outline_space(space, colour)

    def set_persona(self):
        return None