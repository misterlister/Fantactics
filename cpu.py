from units import (
    Unit,
    Peasant,
    Cavalry,
    Sorcerer,
    Archer,
    Archmage,
    General,
    Healer,
    Soldier
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

from player import Player

###### Priority Values

# Terrain

VAL_TERRAIN_BASE = 0
VAL_TERRAIN_FOREST = 1
VAL_TERRAIN_FORTRESS = 2

# Combat

VAL_PEASANT = 2
VAL_SOLDIER = 3
VAL_ARCHER = 3
VAL_SORCERER = 4
VAL_HEALER = 5
VAL_CAVALRY = 5
VAL_ARCHMAGE = 6
VAL_GENERAL = 7

VAL_DEFEAT_GENERAL = 99

PERSONA_ADJUSTMENT = 1.2

######


class AttackTarget:
    def __init__(self, space: Space, unit: Unit, target: Unit) -> None:
        self.space = space
        self.unit = unit
        self.target = target
        self.__value = self.determine_value()
        
    def determine_value(self):
        # Set unit's acting action space
        self.unit.set_action_space(self.space)
        damage_dealt = self.unit.attack_preview(self.target, True)
        damage_taken = self.target.attack_preview(self.unit, False)
        if damage_dealt >= self.target.get_curr_hp():
            # Determine value if the target is defeated
            value = 1
        elif damage_taken >= self.unit.get_curr_hp():
            # Determine value if the unit is lost
            value = 1
        else:
            # Determine the value of the damage exchange
            value = 1
        # Reset unit's action space
        self.unit.reset_action_space()
        return value
    
    def get_value(self):
        return self.__value
    
class AbilityTarget:
    def __init__(self, space: Space, unit: Unit, target: Unit) -> None:
        self.space = space
        self.unit = unit
        self.target = target
        self.__value = self.determine_value()
        
    def determine_value(self):
        
        value = 1
        
        return value
    
    def get_value(self):
        return self.__value
        
class Move_Space:
    def __init__(self, space: Space, unit: Unit, persona: CPU_Persona) -> None:
        self.space = space
        self.unit = unit
        unit.set_action_space(space)
        self.persona = persona
        self.melee_targets = []
        self.ability_targets = []
        self.terrain_value = self.set_terrain_value()
        self.__max_value = self.set_max_value()
        unit.reset_action_space()
    
    def set_terrain_value(self):
        pass
    
    def set_max_value(self):
        pass
    
    def get_max_value(self):
        return self.__max_value
    
    def get_move_value(self):
        # Increase terrain value for Careful CPU
        if self.persona is CPU_Persona.Careful:
            return self.terrain_value * PERSONA_ADJUSTMENT
        return self.terrain_value
        
class Movable_Unit:
    def __init__(self, unit: Unit, persona: CPU_Persona) -> None:
        self.unit = unit
        self.persona = persona
        self.spaces = []
        self.__max_value = self.set_max_value()
        
    def set_max_value(self):
        pass
        
    def get_value(self):
        return self.__max_value
    

class CPU_Player(Player):
    def __init__(self, team: str, difficulty: CPU_Difficulty) -> None:
        super().__init__(team)
        self.__attacking_units: dict[Unit, dict[Space, list[Unit]]] = {}
        self.__ranged_units: dict[Unit, dict[Space, list[Unit]]] = {}
        self.__movable_units: dict[Unit, list[Space]] = {}
        self.__persona: str = self.set_persona()
        self.__difficulty: CPU_Difficulty = difficulty
    
    def take_turn(self) -> None:
        # Disable player board interaction while CPU action executes
        self.get_state().board.unbind_buttons()
        # Choose and execute CPU action
        self.choose_action()
        # Enable player board interaction when CPU is done
        self.get_state().board.bind_buttons()
        
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
        space = None
        if self.__difficulty == CPU_Difficulty.Easy:
            space = random.choice(list(self.__movable_units[unit]))
        else:
            # Get all potential move spaces
            spaces = list(self.__movable_units[unit])  
            
            if self.__persona == CPU_Persona.Aggressive:
                # Aggressive CPU will choose from furthest spaces it can move
                max_row = max(space.get_row() for space in spaces)
                aggressive_spaces = [space for space in spaces if space.get_row() == max_row]
                space = random.choice(aggressive_spaces)
                
            elif self.__persona == CPU_Persona.Careful:
                # Careful CPU will choose to move to the most defensive terrain
                max_defense = max(space.get_defense_mod() for space in spaces)
                careful_spaces = [space for space in spaces if space.get_defense_mod() == max_defense]
                space = random.choice(careful_spaces)
                
            elif self.__persona == CPU_Persona.Balanced:
                # Choose a random space ahead of the current space
                current_row = unit.get_space().get_row()
                balanced_spaces = [space for space in spaces if space.get_row() > current_row]
                # Confirm that a space exists
                if balanced_spaces:
                    space = random.choice(balanced_spaces)
                    
        if space is None:
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
    