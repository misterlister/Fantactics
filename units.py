from math import ceil
from gameBoard import Space
from graphics import SpriteType
from random import randint
from names import Names, Titles
from constants import *

class Unit:
    def __init__(
            self, 
            unit_type: str,
            hp: int, 
            dam_val: int, 
            dam_type: DamageType, 
            arm_val: int, 
            arm_type: ArmourType, 
            move: MoveSpeed, 
            move_type: MoveType,
            sprite,
            name_list,
            title_list,
            ability_name,
            ability_range,
            ability_value
            ) -> None:
        
        self.__unit_type = unit_type
        self.__max_hp = hp
        self.__curr_hp = hp
        self.__damage = dam_val
        self.__damage_type = dam_type
        self.__armour = arm_val
        self.__armour_type = arm_type
        self.__movement = move
        self.__move_type = move_type
        self.__sprite = sprite
        self.__name = self.make_name(name_list, title_list)
        self.__ability_name = ability_name
        self.__ability_range = ability_range
        self.__ability_value = ability_value
        self.__location = None
        self.__dead = False
        self.__player = None
        self.__ability_targets = TARGET_NONE
        self._ability_area_of_effect = []
        
    def get_unit_type(self):
        return self.__unit_type

    def get_max_hp(self):
        return self.__max_hp

    def get_curr_hp(self):
        return self.__curr_hp

    def get_damage_val(self):
        return self.__damage
    
    def get_damage_type(self):
        return self.__damage_type
    
    def get_armour_val(self):
        return self.__armour
    
    def get_armour_type(self):
        return self.__armour_type
    
    def get_movement(self):
        return self.__movement
    
    def get_move_type(self):
        return self.__move_type
    
    def get_player(self):
        return self.__player
    
    def get_sprite(self):
        return self.__sprite
    
    def get_name(self):
        return self.__name
    
    def get_location(self):
        return self.__location
    
    def get_ability_name(self):
        return self.__ability_name
    
    def get_ability_range(self):
        return self.__ability_range
    
    def get_ability_value(self):
        return self.__ability_value
    
    def get_ability_targets(self):
        return self.__ability_targets
    
    def set_ability_targets(self, target_dict: dict):
        self.__ability_targets = target_dict
    
    def set_player(self, player):
        self.__player = player

    def make_name(self, names: list, titles: list) -> str:
        name_index = randint(0, len(names)-1)
        title_index = randint(0, len(titles)-1)
        name = f"{names[name_index]} the {titles[title_index]}"
        del names[name_index]
        del titles[title_index]
        return name

    def move(self, space: Space):
        try:
            if space.get_unit() is None:
                self.__location.assign_unit(None)
                self.__location = space
                space.assign_unit(self)
            else:
                raise Exception("Error: Cannot move unit into another unit's space")
        except Exception as e:
            return e
        
    def _place(self, space: Space):
        self.__location = space

    def take_damage(self, damage: int):
        self.__curr_hp -= damage
        if self.__curr_hp <= 0:
            self.die()

    def heal(self, healing: int):
        if healing + self.__curr_hp > self.__max_hp:
            self.__curr_hp = self.__max_hp
        else:
            self.__curr_hp += healing

    def is_dead(self):
        return self.__dead

    def basic_attack(self, target):
        first_strike_attack = ceil(self.__damage * FIRST_STRIKE_BOOST)
        target_hp = target.get_curr_hp()
        self.attack(target, first_strike_attack, self.__damage_type)
        damage_dealt = target_hp - target.get_curr_hp()
        attack_log = f"{self.get_name()} attacks {target.get_name()}, dealing {damage_dealt} damage!\n"
        return attack_log

    def retaliate(self, target):
        target_hp = target.get_curr_hp()
        self.attack(target, self.__damage, self.__damage_type)
        damage_dealt = target_hp - target.get_curr_hp()
        retaliation_log = f"{self.get_name()} retaliates against {target.get_name()}, dealing {damage_dealt} damage!\n"
        return retaliation_log

    def attack(self, target, damage: int, damage_type):
        effectiveness = weapon_matchup(damage_type, target.get_armour_type())
        atk_damage = damage
        if effectiveness == Effect.STRONG:
            atk_damage = ceil(atk_damage * STRONG_EFFECT_MOD)
        atk_damage -= target.get_armour_val()
        if effectiveness == Effect.POOR:
            atk_damage = ceil(atk_damage * POOR_EFFECT_MOD)
        target.take_damage(atk_damage)

    def special_ability(self, target, space):
        # TEMP
        messages = []
        if target == None or target == self:
            messages.append(f"{self.__name} used {self.__ability_name} on themself")
        else:
            messages.append(f"{self.__name} used {self.__ability_name} on {target.get_name()}")
        return messages
        #

    def die(self):
        self.__dead = True

    def revive(self):
        self.__dead = False

    def choose_action(self):
        print("Choose Action!")
    
    def find_target_spaces(self, space: Space, range: int, target_dict: dict, pass_dict: dict = TARGET_ALL) -> set:
        # Add this space if it is a valid target
        if self.verify_target(space, target_dict):
            target_spaces = {(space.get_row(),space.get_col())}
        else:
            target_spaces = set()
        if range <= 0:
            return target_spaces
        target_spaces = target_spaces.union(self.check_target_spaces(space.get_left(), range, target_dict, pass_dict))
        target_spaces = target_spaces.union(self.check_target_spaces(space.get_up(), range, target_dict, pass_dict))
        target_spaces = target_spaces.union(self.check_target_spaces(space.get_right(), range, target_dict, pass_dict))
        target_spaces = target_spaces.union(self.check_target_spaces(space.get_down(), range, target_dict, pass_dict))
        return target_spaces
    
    def verify_target(self, space: Space, target_dict: dict) -> bool:
        unit = space.get_unit()
        if unit == None: # Check if the space is empty
            if target_dict[TargetType.NONE] == True:
                return True
            else: 
                return False
        if unit == self: # Check if the space is occupied by this unit
            if target_dict[TargetType.ITSELF] == True:
                return True
            else: 
                return False
        if unit.get_player() == self.get_player(): # Check if this space is occupied by an ally
            if target_dict[TargetType.ALLY] == True:
                return True
            else: 
                return False
        else: # The space must be occupied by an enemy
            if target_dict[TargetType.ENEMY] == True:
                return True
            else: 
                return False

    def check_target_spaces(self, space: Space, range: int, target_dict: dict, pass_dict: dict) -> set:
        valid_spaces = set()
        if space != None: # If this space doesn't exist, return
            if self.verify_target(space, pass_dict):
                valid_spaces = valid_spaces.union(self.find_target_spaces(space, range-1, target_dict, pass_dict))
        return valid_spaces
    
    def get_area_of_effect(self, space):
        space_list = []
        space_list.append(space)
        if Direction.UP in self._ability_area_of_effect:
            up_space = space.get_up()
            if up_space != None:
                space_list.append(up_space)
        if Direction.LEFT in self._ability_area_of_effect:
            left_space = space.get_left()
            if left_space != None:
                space_list.append(left_space)
        if Direction.RIGHT in self._ability_area_of_effect:
            right_space = space.get_right()
            if right_space != None:
                space_list.append(right_space)
        if Direction.DOWN in self._ability_area_of_effect:
            down_space = space.get_down()
            if down_space != None:
                space_list.append(down_space)
        return space_list
    
    def adjacent_to(self, unit_type, ally: bool) -> bool:
        location = self.get_location()
        if self.adjacent_direction(location.get_up(), unit_type, ally):
            return True
        if self.adjacent_direction(location.get_left(), unit_type, ally):
            return True
        if self.adjacent_direction(location.get_right(), unit_type, ally):
            return True
        if self.adjacent_direction(location.get_down(), unit_type, ally):
            return True
        return False
    
    def adjacent_direction(self, space, unit_type, ally: bool) -> bool:
        if space != None: # If a space in this direction exists
            if space.contains_unit_type(unit_type): # And it contains a unit
                if self.is_ally(space.get_unit()) == ally: # And that unit matches the ally specification
                    return True
        return False

    def is_unit_type(self, unit_type) -> bool:
        if isinstance(self, unit_type):
            return True
        return False

    def is_ally(self, unit) -> bool:
        if unit.get_player() == self.get_player():
            return True
        return False

        

class Peasant(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "Peasant"
        hp=12
        dam_val=5
        dam_type=DamageType.BLUDGEON
        arm_val=0
        arm_type=ArmourType.PADDED
        move=MoveSpeed.MED
        move_type = MoveType.FOOT
        if p1:
            sprite = SpriteType.PEASANT1
        else:
            sprite = SpriteType.PEASANT2
        name_list = Names.Commoner
        title_list = Titles.Peasant
        ability_name = "Surge of Bravery"
        ability_range = 0
        ability_value = 2
        super().__init__(unit_type, hp, dam_val, dam_type, arm_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_value)
        self.set_ability_targets(TARGET_SELF)
        self.ability_used = False

class Soldier(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "Soldier"
        hp=16
        dam_val=6
        dam_type=DamageType.PIERCE
        arm_val=0#1
        arm_type=ArmourType.CHAIN
        move=MoveSpeed.MED
        move_type = MoveType.FOOT
        if p1:
            sprite = SpriteType.SOLDIER1
        else:
            sprite = SpriteType.SOLDIER2
        name_list = Names.Commoner
        title_list = Titles.Soldier
        ability_name = "Guarded Advance" 
        ability_range = 1
        ability_value = None
        super().__init__(unit_type, hp, dam_val, dam_type, arm_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_value)
        self.set_ability_targets(TARGET_ALLIES)

    def special_ability(self, target, space):
        unit_name = self.get_name()
        target_name = target.get_name()
        attack_log = []
        current_space = self.get_location()
        current_space.assign_unit(None)
        target.move(current_space)
        space.assign_unit(self)
        self.move(space)
        attack_log.append(f"{unit_name} moves to defend {target_name}, taking their place.\n")
        attack_log.append(f"{unit_name} -> {space.get_row()},{space.get_col()}.\n")
        attack_log.append(f"{target_name} -> {current_space.get_row()},{current_space.get_col()}.\n")
        return attack_log

class Archer(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "Archer"
        hp=15
        dam_val=4
        dam_type=DamageType.PIERCE
        arm_val=0
        arm_type=ArmourType.PADDED
        move=MoveSpeed.MED
        move_type = MoveType.FOOT
        if p1:
            sprite = SpriteType.ARCHER1
        else:
            sprite = SpriteType.ARCHER2
        name_list = Names.Commoner
        title_list = Titles.Archer
        ability_name = "Ranged Attack"
        ability_range = 5
        ability_value = 6
        super().__init__(unit_type, hp, dam_val, dam_type, arm_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_value)
        self.set_ability_targets(TARGET_ENEMIES)
        self.__special_damage_type = DamageType.PIERCE

    def special_ability(self, target, space):
        unit_name = self.get_name()
        target_name = target.get_name()
        attack_log = []
        first_strike_attack = ceil(self.get_ability_value() * FIRST_STRIKE_BOOST)
        target_hp = target.get_curr_hp()
        self.attack(target, first_strike_attack, self.__special_damage_type)
        damage_dealt = target_hp - target.get_curr_hp()
        attack_log.append(f"{unit_name} fires an arrow at {target_name}, dealing {damage_dealt} damage!\n")
        if target.is_dead():
            attack_log.append(f"{unit_name} has slain {target_name}!\n")
            target.get_location().assign_unit(None)
        return attack_log

class Cavalry(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "Cavalry"
        hp=18
        dam_val=7
        dam_type=DamageType.SLASH
        arm_val=0#1
        arm_type=ArmourType.PLATE
        move=MoveSpeed.FAST
        move_type = MoveType.HORSE
        if p1:
            sprite = SpriteType.PEASANT1
        else:
            sprite = SpriteType.PEASANT2
        name_list = Names.Noble
        title_list = Titles.Cavalry
        ability_name = "Harrying Strike"
        ability_range = 0
        ability_value = None
        super().__init__(unit_type, hp, dam_val, dam_type, arm_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_value)
        self.set_ability_targets(TARGET_SELF)
    
    # Variation of movement calculation that allows for passing all units except Enemy-aligned Soldiers
    def check_target_spaces(self, space: Space, range: int, target_dict: dict, pass_dict: dict) -> set:
        valid_spaces = set()
        if space != None: # If this space doesn't exist, return
            target = space.get_unit()
            if target_dict != TARGET_ENEMIES: # If this is not an attack
                if target != None: # If there is a unit here
                    if target.get_player() != self.get_player(): # And this unit is an enemy
                        if isinstance(target, Soldier): # And that enemy is a Soldier Class
                            return valid_spaces # Do not proceed
            valid_spaces = valid_spaces.union(self.find_target_spaces(space, range-1, target_dict, pass_dict))
        return valid_spaces
    
class Sorcerer(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "Sorcerer"
        hp=14
        dam_val=4
        dam_type=DamageType.PIERCE
        arm_val=0
        arm_type=ArmourType.ROBES
        move=MoveSpeed.MED
        move_type = MoveType.FOOT
        if p1:
            sprite = SpriteType.SORCERER1
        else:
            sprite = SpriteType.SORCERER2
        name_list = Names.Mage
        title_list = Titles.Sorcerer
        ability_name = "Sorcerous Assault"    
        ability_range = 4
        ability_value = 6
        super().__init__(unit_type, hp, dam_val, dam_type, arm_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_value)
        self.set_ability_targets(TARGET_ALL)
        self.__special_damage_type = DamageType.MAGIC
        self._ability_area_of_effect.extend([Direction.LEFT, Direction.RIGHT])
        

    def special_ability(self, target, space):
        attack_log = []
        left_space = space.get_left()
        if left_space is not None:
            left_target = left_space.get_unit()
            if left_target != None:
                attack_log += (self.magic_power(left_target))
        attack_log += (self.magic_power(target))
        right_space = space.get_right()
        if right_space is not None:
            right_target = right_space.get_unit()
            if right_target != None:
                attack_log += (self.magic_power(right_target))
        if len(attack_log) == 0:
            attack_log.append(f"{self.get_name()} blasts the darkness with arcane energy. It has no effect!\n")
        return attack_log
        
    def magic_power(self, target):
        unit_name = self.get_name()
        if target is self:
            target_name = "themself"
        else:
            target_name = target.get_name()
        attack_log = []
        damage = self.get_ability_value()
        target_hp = target.get_curr_hp()
        self.attack(target, damage, self.__special_damage_type)
        damage_dealt = target_hp - target.get_curr_hp()
        attack_log.append(f"{unit_name} blasts {target_name} with arcane energy, dealing {damage_dealt} damage!\n")
        if target.is_dead():
            attack_log.append(f"{unit_name} has slain {target_name}!\n")
            target.get_location().assign_unit(None)
        return attack_log

class Healer(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "Healer"
        hp=15
        dam_val=6
        dam_type=DamageType.BLUDGEON
        arm_val=0#1
        arm_type=ArmourType.CHAIN
        move=MoveSpeed.MED
        move_type = MoveType.FOOT
        if p1:
            sprite = SpriteType.HEALER1
        else:
            sprite = SpriteType.HEALER2
        name_list = Names.Mage
        title_list = Titles.Healer
        ability_name = "Healing Radiance"
        ability_range = 0
        ability_value = 5
        super().__init__(unit_type, hp, dam_val, dam_type, arm_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_value)
        self.set_ability_targets(TARGET_SELF)
        self._ability_area_of_effect.extend([Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN])

    def special_ability(self, target, space):
        attack_log = []
        top_space = space.get_up()
        if top_space is not None:
            top_target = top_space.get_unit()
            if top_target != None:
                attack_log += (self.magic_power(top_target))
        left_space = space.get_left()
        if left_space is not None:
            left_target = left_space.get_unit()
            if left_target != None:
                attack_log += (self.magic_power(left_target))
        attack_log += (self.magic_power(target))
        right_space = space.get_right()
        if right_space is not None:
            right_target = right_space.get_unit()
            if right_target != None:
                attack_log += (self.magic_power(right_target))
        down_space = space.get_down()
        if down_space is not None:
            down_target = down_space.get_unit()
            if down_target != None:
                attack_log += (self.magic_power(down_target))
        if len(attack_log) == 0:
            attack_log.append(f"{self.get_name()} infuses their surroundings with healing magic. The warmth is pleasant, but it has no effect!\n")
        return attack_log
        
    def magic_power(self, target):
        if self.get_player() == target.get_player():
            unit_name = self.get_name()
            target_name = target.get_name()
            attack_log = []
            target_hp = target.get_curr_hp()
            target.heal(self.get_ability_value())
            damage_healed = target.get_curr_hp() - target_hp
            if damage_healed > 0:
                attack_log.append(f"{unit_name} infuses {target_name} with mystical energy, healing {damage_healed} damage!\n")
        return attack_log

class Archmage(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "Archmage"
        hp=22
        dam_val=5
        dam_type=DamageType.BLUDGEON
        arm_val=0
        arm_type=ArmourType.ROBES
        move=MoveSpeed.MED
        move_type = MoveType.FLY
        if p1:
            sprite = SpriteType.ARCHMAGE1
        else:
            sprite = SpriteType.ARCHMAGE2
        name_list = Names.Mage
        title_list = Titles.Archmage
        ability_name = "Arcane Vortex"
        ability_range = 3
        ability_value = 7
        super().__init__(unit_type, hp, dam_val, dam_type, arm_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_value)
        self.set_ability_targets(TARGET_ALL)
        self.__special_damage_type = DamageType.MAGIC
        self._ability_area_of_effect.extend([Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN])

    def special_ability(self, target, space):
        attack_log = []
        top_space = space.get_up()
        if top_space is not None:
            top_target = top_space.get_unit()
            if top_target is not None:
                attack_log += (self.magic_power(top_target))
        left_space = space.get_left()
        if left_space is not None:
            left_target = left_space.get_unit()
            if left_target is not None:
                attack_log += (self.magic_power(left_target))
        if target is not None:
            attack_log += (self.magic_power(target))
        right_space = space.get_right()
        if right_space is not None:
            right_target = right_space.get_unit()
            if right_target != None:
                attack_log += (self.magic_power(right_target))
        down_space = space.get_down()
        if down_space is not None:
            down_target = down_space.get_unit()
            if down_target != None:
                attack_log += (self.magic_power(down_target))
        if len(attack_log) == 0:
            attack_log.append(f"{self.get_name()} blasts the darkness with arcane energy. It has no effect!\n")
        return attack_log
        
    def magic_power(self, target):
        unit_name = self.get_name()
        if target is self:
            target_name = "themself"
        else:
            target_name = target.get_name()
        attack_log = []
        damage = self.get_ability_value()
        target_hp = target.get_curr_hp()
        self.attack(target, damage, self.__special_damage_type)
        damage_dealt = target_hp - target.get_curr_hp()
        attack_log.append(f"{unit_name} blasts {target_name} with arcane energy, dealing {damage_dealt} damage!\n")
        if target.is_dead():
            attack_log.append(f"{unit_name} has slain {target_name}!\n")
            target.get_location().assign_unit(None)
        return attack_log

class General(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "General"
        hp=24
        dam_val=8
        dam_type=DamageType.SLASH
        arm_val=0#2
        arm_type=ArmourType.PLATE
        move=MoveSpeed.SLOW
        move_type = MoveType.FOOT
        if p1:
            sprite = SpriteType.GENERAL1
        else:
            sprite = SpriteType.GENERAL2
        name_list = Names.Noble
        title_list = Titles.General
        ability_name = "Inspirational Rally"
        ability_range = 0
        ability_value = 1
        super().__init__(unit_type, hp, dam_val, dam_type, arm_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_value)
        self.set_ability_targets(TARGET_SELF)
        self.ability_used = False


def weapon_matchup(weapon, armour):
    if weapon == DamageType.SLASH:
        if armour == ArmourType.ROBES:
            return Effect.STRONG
        elif armour == ArmourType.PADDED:
            return Effect.STRONG
        elif armour == ArmourType.CHAIN:
            return Effect.POOR
        elif armour == ArmourType.PLATE:
            return Effect.POOR
        
    elif weapon == DamageType.PIERCE:
        if armour == ArmourType.ROBES:
            return Effect.STRONG
        elif armour == ArmourType.PADDED:
            return Effect.NEUTRAL
        elif armour == ArmourType.CHAIN:
            return Effect.NEUTRAL
        elif armour == ArmourType.PLATE:
            return Effect.POOR
        
    elif weapon == DamageType.BLUDGEON:
        if armour == ArmourType.ROBES:
            return Effect.NEUTRAL
        elif armour == ArmourType.PADDED:
            return Effect.NEUTRAL
        elif armour == ArmourType.CHAIN:
            return Effect.NEUTRAL
        elif armour == ArmourType.PLATE:
            return Effect.NEUTRAL
        
    elif weapon == DamageType.MAGIC:
        if armour == ArmourType.ROBES:
            return Effect.POOR
        elif armour == ArmourType.PADDED:
            return Effect.NEUTRAL
        elif armour == ArmourType.CHAIN:
            return Effect.NEUTRAL
        elif armour == ArmourType.PLATE:
            return Effect.STRONG
        
    return None
