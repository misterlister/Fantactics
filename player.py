from units import (
    Unit,
    Peasant,
    Cavalry,
    Sorcerer,
    Archer,
    Archmage
    )

import random

from space import Space

from constants import (
    CPU_DELAY,
    SELECT_COL,
    ACTION_COL,
    ATTACK_COL,
    ABILITY_COL,
    CPU_Persona,
    CPU_Difficulty
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
    def __init__(self, team: str, difficulty: CPU_Difficulty) -> None:
        super().__init__(team)
        self.__attacking_units: dict[Unit, dict[Space, list[Unit]]] = {}
        self.__ranged_units: dict[Unit, dict[Space, list[Unit]]] = {}
        self.__movable_units: dict[Unit, list[Space]] = {}
        self.__persona: str = self.set_persona()
        self.__difficulty: CPU_Difficulty = difficulty
    
    def take_turn(self) -> None:
        self.choose_action()
        
    def choose_action(self):
        self.get_attacking_units()
        self.get_ranged_units()
        # If there are no targets to attack, move a unit instead
        if len(self.__attacking_units) == 0 and len(self.__ranged_units) == 0:
            self.get_movable_units()
            unit, space = self.choose_move_target()
            self.get_state().board.draw_all_spaces()
            self.move_unit(unit, space)
        else:
            melee_attack = self.choose_if_melee_attack()
            if melee_attack:
                unit = self.choose_attacker(self.__attacking_units)
                target, space = self.choose_attack_target(unit, self.__attacking_units)
                if self.choose_if_activate_melee_ability(unit, target):
                    attack_type = self.attack_action
                else:
                    attack_type = self.ability_action
                self.get_state().board.draw_all_spaces()
                attack_type(unit, target, space)
            else:
                unit = self.choose_attacker(self.__ranged_units)
                target, space = self.choose_attack_target(unit, self.__ranged_units)
                self.get_state().board.draw_all_spaces()
                self.ability_action(unit, target, space)
        
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
            
    def get_ranged_units(self):
        self.__ranged_units = {}
        for unit in self.get_unit_list():
            # Check if the unit has a ranged ability (Sorcerer, Archer, Archmage)
            if isinstance(unit, (Sorcerer, Archer, Archmage)):
                # Check that the unit's ability isn't disabled
                if not unit.ability_disabled():
                    spaces = self.get_state().board.get_movement_spaces(unit, unit.get_space())
                    targetable_spaces = {} # Temporary dictionary to hold valid attackable spaces
                    
                    for space in spaces:
                        if space is not None:
                            targets = self.get_state().board.get_ability_spaces(unit, space)
                            valid_targets = []
                            for target in targets:
                                if target is not None:
                                    target_unit = target.get_unit()
                                    if target_unit is not None and target_unit.get_player() != self:
                                        valid_targets.append(target)
                            
                            if len(valid_targets) > 0: # Only add spaces that have valid attack targets
                                targetable_spaces[space] = valid_targets
                            
                    if len(targetable_spaces) > 0: # Only add units that have at least one target
                        self.__ranged_units[unit] = targetable_spaces
            
    def get_movable_units(self):
        self.__movable_units = {}
        for unit in self.get_unit_list():
            current_space = unit.get_space()
            spaces = self.get_state().board.get_movement_spaces(unit, unit.get_space())
            if current_space in spaces: # Remove the unit's current space from movement options
                spaces.remove(current_space)
            if len(spaces) > 0: # Only add this unit if it has at least one space to move to
                self.__movable_units[unit] = spaces
    
    def choose_move_target(self):
        unit = random.choice(list(self.__movable_units.keys()))
        space = random.choice(list(self.__movable_units[unit]))
        return unit, space
    
    def move_unit(self, unit: Unit, space: Space):
        # Highlight the selected unit's space
        self.select_space(unit.get_space(), SELECT_COL)
        # Schedule highlighting of destination after a delay
        self.get_state().board.root.after(CPU_DELAY, self.highlight_move_space, unit, space)
        
    def highlight_move_space(self, unit: Unit, space: Space):
        # Highlight the selected destination space
        self.select_space(space, ACTION_COL)
        # Schedule movement execution after a delay
        self.get_state().board.root.after(CPU_DELAY, self.execute_move, unit, space)
    
    def execute_move(self, unit: Unit, space: Space):
        self.get_state().board.move_and_wait(unit, space)
        
    def choose_if_melee_attack(self):
        if len(self.__attacking_units) == 0:
            return False
        if len(self.__ranged_units) == 0:
            return True
        if self.__persona == CPU_Persona.Careful:
            return False
        if self.__persona == CPU_Persona.Aggressive:
            return True
        if random.randint(0,1) == 1:
            return True
        return False
    
    def choose_attacker(self, attacker_dict):
        unit = random.choice(list(attacker_dict.keys()))
        return unit
        
    def choose_attack_target(self, unit: Unit, attacker_dict):
        target_options = []

        # Collect all attackable targets from all spaces
        for space, enemies in attacker_dict[unit].items():
            for enemy in enemies:
                target_options.append((enemy, space))  # Store the enemy and the space
        
        # Randomly select a target from the list of options
        if target_options:
            chosen_enemy, chosen_space = random.choice(target_options)
            return chosen_enemy, chosen_space
        else:
            return None, None  # No valid targets
        
    def attack_action(self, unit: Unit, target: Space, move_space: Space):
        self.highlight_selected_unit(unit, target, move_space, self.highlight_target)
        
    def ability_action(self, unit: Unit, target: Space, move_space: Space):
        self.highlight_selected_unit(unit, target, move_space, self.highlight_ability_target)
        
    def highlight_selected_unit(self, unit: Unit, target: Space, move_space: Space, execution_function):
        # Highlight the selected unit's space
        self.select_space(unit.get_space(), SELECT_COL)
        # Schedule highlighting of the movement space after a delay
        self.get_state().board.root.after(CPU_DELAY, self.highlight_new_location, unit, target, move_space, execution_function)
        
    def highlight_new_location(self, unit: Unit, target: Space, move_space: Space, execution_function):    
        # Highlight the selected destination space
        self.select_space(move_space, ACTION_COL)
        # Schedule highlighting of the target's space after a delay
        self.get_state().board.root.after(CPU_DELAY, execution_function, unit, target, move_space)
    
    def highlight_target(self, unit: Unit, target: Space, move_space: Space):
        # Highlight the target's space
        self.select_space(target, ATTACK_COL)
        # Execute attack after a delay
        self.get_state().board.root.after(CPU_DELAY, self.execute_attack, unit, target, move_space)
        
    def highlight_ability_target(self, unit: Unit, target: Space, move_space: Space):
        # Highlight the target's space
        self.select_space(target, ABILITY_COL)
        # Execute ability attack after a delay
        self.get_state().board.root.after(CPU_DELAY, self.execute_ability, unit, target, move_space)
        
    def execute_attack(self, unit: Unit, target: Space, move_space: Space):
        self.get_state().board.attack_action(unit, target, move_space)
        
    def execute_ability(self, unit: Unit, target: Space, move_space: Space):
        self.get_state().board.ability_action(unit, target, move_space)
        
    def choose_if_activate_melee_ability(self, unit: Unit, target: Unit) -> bool:
        # Check if the unit has a melee ability (Peasant or Cavalry)
        if isinstance(unit, (Peasant, Cavalry)):
            # Check if the ability is disabled or expended first
            if not unit.ability_disabled() and not unit.ability_expended():
                # Randomly choose between ability_action and attack_action
                return False if random.randint(0, 1) == 1 else True
        
        # Default action if ability is unavailable or unit doesn't have one
        return True
             
    def select_space(self, space: Space, colour: str):
        if colour == ATTACK_COL or colour == ACTION_COL or colour == SELECT_COL or colour == ABILITY_COL:
            self.get_state().board.outline_space(space, colour)

    def set_persona(self):
        return random.choice(list(CPU_Persona))