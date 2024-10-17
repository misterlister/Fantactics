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

from space import Space, Forest, Fortress

from constants import (
    CPU_DELAY,
    SELECT_COL,
    ACTION_COL,
    ATTACK_COL,
    ABILITY_COL,
    CPU_Persona,
    CPU_Difficulty,
    BOARD_ROWS
)

from player import Player

###### Priority Values

# Terrain

VAL_TERRAIN_BASE = 0
VAL_TERRAIN_FOREST = 1
VAL_TERRAIN_FORTRESS = 2
VAL_PEASANT_PROMOTE = 3

VAL_ADVANCE_ROWS = 1

# Combat
COMBAT_VAL = {
    Peasant: 2,
    Soldier: 3,
    Archer: 3,
    Sorcerer: 4,
    Healer: 5,
    Cavalry: 5,
    Archmage: 6,
    General: 7
}

PEASANT_ABILITY_MOD = -0.5

VAL_DEFEAT_GENERAL = 99

PERSONA_ADJUSTMENT = 1.2

######

class Persona:
    
    def generate_combat_value(self, unit: Unit, target: Unit, space: Space, damage_dealt: int, damage_taken: int, secondary_attack: bool = False):
        value = 0
        
        if damage_dealt >= target.get_curr_hp():
            # Value if the target is defeated
            value += self.generate_combat_victory_value(target, space, secondary_attack)
        elif damage_taken >= unit.get_curr_hp():
            # Value if the unit is lost
            value += self.generate_combat_loss_value(unit, target, damage_dealt)
        else:
            # Value of the damage exchange
            value += self.generate_combat_stalemate_value(unit, target, space, damage_dealt, damage_taken, secondary_attack)
        return value
    
    def generate_combat_victory_value(self, unit: Unit, target: Unit, space: Space, secondary_attack: bool = False):
        if isinstance(target, General):
            return VAL_DEFEAT_GENERAL
        if secondary_attack:
            terrain_value = 0
        else:
            terrain_value = self.movement_value(unit, space)
        defeat_value = self.target_defeat_value(target)
        combat_victory_value = terrain_value + defeat_value
        return combat_victory_value
        
    def generate_combat_loss_value(self, unit: Unit, target: Unit, damage_dealt: int):
        damage_value = self.target_damage_value(target, damage_dealt)
        loss_value = self.unit_loss_value(unit)
        combat_loss_value = damage_value - loss_value
        return combat_loss_value
    
    def generate_combat_stalemate_value(self, unit: Unit, target: Unit, space: Space, damage_dealt: int, damage_taken: int, secondary_attack: bool = False):
        if secondary_attack:
            terrain_value = 0
        else:
            terrain_value = self.movement_value(unit, space)
        target_damage_value = self.target_damage_value(target, damage_dealt)
        if damage_taken == 0:
            unit_damage_value = 1
        else:
            unit_damage_value = self.unit_damage_value(unit, damage_taken)
        combat_outcome_value = 2 * (target_damage_value / unit_damage_value)
        overall_value = terrain_value + combat_outcome_value
        return overall_value
    
    def generate_ability_value(self, unit: Unit, target: Unit, space: Space):
        value = 0
        match unit:
            case Peasant():
                value = self.peasant_ability_value(unit, target, space)
            case Soldier():
                value = self.soldier_ability_value(unit, target, space)
            case Cavalry():
                value = self.cavalry_ability_value(unit, target, space)
            case Sorcerer():
                value = self.sorcerer_ability_value(unit, target, space)
            case Archmage():
                value = self.archmage_ability_value(unit, target, space)
            case Archer():
                value = self.archer_ability_value(unit, target, space)
            case General():
                value = self.general_ability_value(unit, target, space)
            case Healer():
                value = self.healer_ability_value(unit, target, space)
            case _:
                print("Error: unit type not matching for ability value checking")
        return value
    
    def peasant_ability_value(self, unit: Unit, target: Unit, space: Space):
        # Reduce combat value by the peasant ability modifier to reflect cost of using ability
        value = PEASANT_ABILITY_MOD
        damage_dealt, damage_taken = unit.ability_preview(target)
        value += self.generate_combat_value(unit, target, space, damage_dealt, damage_taken)
        return value
    
    def soldier_ability_value(self, unit: Unit, target: Unit, space: Space):
        # Grant 1/2 of a unit's value if that unit is injured and not adjacent to a Soldier
        if isinstance(target, (General, Archer, Archmage, Sorcerer)): 
            if not target.adjacent_to(Soldier, True):
                if target.__curr_hp < target.__max_hp()/2:
                    return COMBAT_VAL[type(target)] / 2
        return 0
    
    def cavalry_ability_value(self, unit: Unit, target: Unit, space: Space):
        # Increase combat value if the foe is a high-priority ability target
        value = 0
        if isinstance(target, (Healer, Archer, Archmage, Sorcerer)): 
            value += COMBAT_VAL[type(target)] / 3
        damage_dealt, damage_taken = unit.ability_preview(target)
        value += self.generate_combat_value(unit, target, space, damage_dealt, damage_taken)
        return value
    
    def sorcerer_ability_value(self, unit: Unit, target: Unit, space: Space):
        value = 0
        # Calculate main target damage
        damage_dealt, damage_taken = unit.ability_preview(target)
        # Disregard damage taken
        damage_taken = 0
        value += self.generate_combat_value(unit, target, space, damage_dealt, damage_taken)
        # Add left space splash value
        value += self.get_splash_damage_value(unit, space.get_left())
        # Add right space splash value
        value += self.get_splash_damage_value(unit, space.get_right())
        return value
    
    def archmage_ability_value(self, unit: Unit, target: Unit, space: Space):
        value = 0
        # Calculate main target damage
        damage_dealt, damage_taken = unit.ability_preview(target)
        # Disregard damage taken
        damage_taken = 0
        value += self.generate_combat_value(unit, target, space, damage_dealt, damage_taken)
        # Add left space splash value
        value += self.get_splash_damage_value(unit, space.get_left())
        # Add right space splash value
        value += self.get_splash_damage_value(unit, space.get_right())
        # Add upper space splash value
        value += self.get_splash_damage_value(unit, space.get_up())
        # Add lower space splash value
        value += self.get_splash_damage_value(unit, space.get_down())
        return value
    
    def archer_ability_value(self, unit: Unit, target: Unit, space: Space):
        # Calculate target damage
        damage_dealt, damage_taken = unit.ability_preview(target)
        value = self.generate_combat_value(unit, target, space, damage_dealt, damage_taken)
        return value
    
    def general_ability_value(self, unit: Unit, target: Unit, space: Space):
        # Create value that increases as the game goes on longer
        turn_number = unit.get_player().get_state().get_turn()
        val = random.randint(1,50)
        if val < turn_number:
            value = VAL_DEFEAT_GENERAL
        else:
            value = 1
        return value
    
    def healer_ability_value(self, unit: Unit, target: Unit, space: Space):
        # Calculate target damage
        terrain_value = self.movement_value(unit, space)
        heal_value = 0
        heal_value += self.get_heal_value(unit, space.get_left())
        heal_value += self.get_heal_value(unit, space.get_right())
        heal_value += self.get_heal_value(unit, space.get_up())
        heal_value += self.get_heal_value(unit, space.get_down())
        value = heal_value + terrain_value
        return value
    
    def get_heal_value(self, unit: Unit, space: Space):
        if space is None:
            return 0
        
        target = space.get_unit()
        
        if target == None:
            return 0
        
        if unit.get_player() != target.get_player():
            return 0
        
        ability_value = unit.get_ability_value()
        
        target_missing_hp = target.get_max_hp() - target.get_curr_hp()
        
        heal_amount = min(ability_value, target_missing_hp)
        
        if heal_amount < 1:
            return 0
        
        value = (heal_amount / target.get_max_hp()) * COMBAT_VAL[type(target)]
        
        return value
        
    
    def get_splash_damage_value(self, unit: Unit, space: Space):
        if space is None:
            return 0
        
        target = space.get_unit()
        
        if target == None:
            return 0
        
        splash_damage = unit.ability_splash_preview(target)
        if splash_damage == 0:
            return
        
        value = self.generate_combat_value(unit, target, space, splash_damage, 0, True)
        
        if unit.get_player() == target.get_player():
            value = -value
            
        return value
    
    def movement_value(self, unit: Unit, space: Space):
        move_value = VAL_TERRAIN_BASE
        if isinstance(space.get_terrain(), Forest):
            move_value += VAL_TERRAIN_FOREST
        elif isinstance(space.get_terrain(), Fortress):
            move_value += VAL_TERRAIN_FORTRESS
            
        if space.get_row() > unit.get_space().get_row():
            move_value += VAL_ADVANCE_ROWS
        if isinstance(unit, Peasant) and space.get_row() == BOARD_ROWS -1:
            move_value += VAL_PEASANT_PROMOTE
            
        return move_value
    
    def target_damage_value(self, target: Unit, damage_dealt: int):
        target_hp = target.get_curr_hp()
        damage_fraction = damage_dealt / target_hp
        damage_value = damage_fraction * COMBAT_VAL[type(target)]
        return damage_value
    
    def target_defeat_value(self, target: Unit):
        defeat_value = COMBAT_VAL[type(target)]
        return defeat_value
    
    def unit_damage_value(self, unit: Unit, damage_taken: int):
        unit_hp = unit.get_curr_hp()
        damage_fraction = damage_taken / unit_hp
        damage_value = damage_fraction * COMBAT_VAL[type(unit)]
        return damage_value
    
    def unit_loss_value(self, unit: Unit):
        loss_value = COMBAT_VAL[type(unit)]
        return loss_value
    
    
class AggressivePersona(Persona):
    
    # Increase value of advancing forwards
    def movement_value(self, unit: Unit, space: Space):
        move_value = VAL_TERRAIN_BASE
        if isinstance(space.get_terrain(), Forest):
            move_value += VAL_TERRAIN_FOREST
        elif isinstance(space.get_terrain(), Fortress):
            move_value += VAL_TERRAIN_FORTRESS
            
        if space.get_row() > unit.get_space().get_row():
            move_value += VAL_ADVANCE_ROWS * PERSONA_ADJUSTMENT
            
        if isinstance(unit, Peasant) and space.get_row() == BOARD_ROWS -1:
            move_value += VAL_PEASANT_PROMOTE
            
        return move_value
    
    # Increase value of damaging targets
    def target_damage_value(self, target: Unit, damage_dealt: int):
        target_hp = target.get_curr_hp()
        damage_fraction = damage_dealt / target_hp
        damage_value = damage_fraction * COMBAT_VAL[type(target)] * PERSONA_ADJUSTMENT
        return damage_value
    
    # Increase value of defeating targets
    def target_defeat_value(self, target: Unit):
        defeat_value = COMBAT_VAL[type(target)] * PERSONA_ADJUSTMENT
        return defeat_value
    
class CarefulPersona(Persona):
    
    # Add extra value to defensive terrain
    def movement_value(self, unit: Unit, space: Space):
        move_value = VAL_TERRAIN_BASE
        if isinstance(space.get_terrain(), Forest):
            move_value += VAL_TERRAIN_FOREST * PERSONA_ADJUSTMENT
        elif isinstance(space.get_terrain(), Fortress):
            move_value += VAL_TERRAIN_FORTRESS * PERSONA_ADJUSTMENT
            
        if space.get_row() > unit.get_space().get_row():
            move_value += VAL_ADVANCE_ROWS
            
        if isinstance(unit, Peasant) and space.get_row() == BOARD_ROWS -1:
            move_value += VAL_PEASANT_PROMOTE
            
        return move_value
    
    # Increase negative value of units receiving damage
    def unit_damage_value(self, unit: Unit, damage_taken: int):
        unit_hp = unit.get_curr_hp()
        damage_fraction = damage_taken / unit_hp
        damage_value = damage_fraction * COMBAT_VAL[type(unit)] * PERSONA_ADJUSTMENT
        return damage_value
    
    # Increase negative value of losing units
    def unit_loss_value(self, unit: Unit):
        loss_value = COMBAT_VAL[type(unit)] * PERSONA_ADJUSTMENT
        return loss_value

    # Increase value of ranged attacks and healing
    def generate_ability_value(self, unit: Unit, target: Unit, space: Space):
        value = 0
        match unit:
            case Peasant():
                value = self.peasant_ability_value(unit, target, space)
            case Soldier():
                value = self.soldier_ability_value(unit, target, space)
            case Cavalry():
                value = self.cavalry_ability_value(unit, target, space)
            case Sorcerer():
                value = self.sorcerer_ability_value(unit, target, space) * PERSONA_ADJUSTMENT
            case Archmage():
                value = self.archmage_ability_value(unit, target, space) * PERSONA_ADJUSTMENT
            case Archer():
                value = self.archer_ability_value(unit, target, space) * PERSONA_ADJUSTMENT
            case General():
                value = self.general_ability_value(unit, target, space)
            case Healer():
                value = self.healer_ability_value(unit, target, space) * PERSONA_ADJUSTMENT
            case _:
                print("Error: unit type not matching for ability value checking")
        return value


class AttackTarget:
    def __init__(self, space: Space, unit: Unit, target: Unit, persona: Persona) -> None:
        self.space = space
        self.unit = unit
        self.target = target
        self.persona = persona
        self.__value = self.determine_value()

    def determine_value(self):
        # Set unit's acting action space
        self.unit.set_action_space(self.space)
        damage_dealt = self.unit.attack_preview(self.target, True)
        damage_taken = self.target.attack_preview(self.unit, False)
        value = self.persona.generate_combat_value(self.unit, self.target, self.space, damage_dealt, damage_taken)
        # Reset unit's action space
        self.unit.reset_action_space()
        return value

    def get_value(self):
        return self.__value

class AbilityTarget:
    def __init__(self, space: Space, unit: Unit, target: Unit, persona: Persona) -> None:
        self.space = space
        self.unit = unit
        self.target = target
        self.persona = persona
        self.__value = self.determine_value()

    def determine_value(self):
        # Set unit's action space
        self.unit.set_action_space(self.space)
        value = self.persona.generate_ability_value(self.unit, self.target, self.space)
        # Reset unit's action space
        self.unit.reset_action_space()
        return value

    def get_value(self):
        return self.__value

class MoveSpace:
    def __init__(self, space: Space, unit: Unit, persona: Persona, board) -> None:
        self.space = space
        self.unit = unit
        unit.set_action_space(space)
        self.persona = persona
        self.board = board
        self.attack_targets = self.find_attack_targets()
        self.ability_targets = self.find_ability_targets()
        self.move_value = persona.movement_value(self.unit, self.space)
        self.__max_value = self.set_max_value()
        unit.reset_action_space()
    
    def set_max_value(self):
        self.sort_ability_targets()
        self.sort_attack_targets()
        if len(self.attack_targets > 0):
            attackMax = self.attack_targets[0].get_value()
        else:
            attackMax = 0
        if len(self.ability_targets > 0):
            abilityMax = self.ability_targets[0].get_value()
        else:
            abilityMax = 0
        return max(attackMax, abilityMax, self.move_value)

    def get_value(self):
        return self.__max_value

    def find_attack_targets(self):
        attack_targets = []
        targets = self.board.get_attack_spaces(self.unit, self.space)

        for target in targets:
            target_unit = target.get_unit()
            if target_unit is not None:
                new_target = AttackTarget(self.space, self.unit, target_unit, self.persona)
                attack_targets.append(new_target)

        return attack_targets

    def sort_attack_targets(self):
        # Sort attack_targets by their value in descending order
        self.attack_targets.sort(key=lambda target: target.get_value(), reverse=True)

    def find_ability_targets(self):
        ability_targets = []
        targets = self.board.get_ability_spaces(self.unit, self.space)

        for target in targets:
            target_unit = target.get_unit()
            if target_unit is not None:
                new_target = AbilityTarget(self.space, self.unit, target_unit, self.persona)
                ability_targets.append(new_target)

        return ability_targets

    def sort_ability_targets(self):
        # Sort ability_targets by their value in descending order
        self.ability_targets.sort(key=lambda target: target.get_value(), reverse=True)


class MovableUnit:
    def __init__(self, unit: Unit, persona: Persona, board) -> None:
        self.unit = unit
        self.persona = persona
        self.board = board
        self.move_spaces = self.find_spaces()
        self.__max_value = self.set_max_value()
        
    def set_max_value(self):
        self.sort_move_spaces()
        if len(self.move_spaces > 0):
            spaceMax = self.move_spaces[0].get_value()
        else:
            spaceMax = 0
        return spaceMax
        
    def sort_move_spaces(self):
        # Sort attack_targets by their value in descending order
        self.move_spaces.sort(key=lambda target: target.get_value(), reverse=True)
        
    def get_value(self):
        return self.__max_value
    
    def find_spaces(self):
        move_spaces = []
        spaces = self.board.get_movement_spaces(self.unit, self.unit.get_space())

        for space in spaces:
            new_space = MoveSpace(space, self.unit, self.persona, self.board)
            move_spaces.append(new_space)

        return move_spaces
    
    def choose_space(self, difficulty: CPU_Difficulty):
        if difficulty == CPU_Difficulty.Easy:
            pass

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
    