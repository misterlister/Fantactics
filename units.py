from enum import IntEnum
from math import ceil
from gameBoard import Space, BOARD_ROWS, BOARD_COLS
from graphics import SpriteType
from random import randint
from names import Names, Titles

FIRST_STRIKE_BOOST = 1.2
POOR_EFFECT_MOD = 4/5
STRONG_EFFECT_MOD = 5/4

class DamageType(IntEnum):
    SLASH = 1
    PIERCE = 2
    BLUDGEON = 3
    MAGIC = 4

class ArmourType(IntEnum):
    ROBES = 1
    PADDED = 2
    CHAIN = 3
    PLATE = 4

class Effect(IntEnum):
    POOR = 1
    NEUTRAL = 2
    STRONG = 3

class MoveSpeed(IntEnum):
    SLOW = 2
    MED = 3
    FAST = 4

class MoveType(IntEnum):
    FOOT = 1
    HORSE = 2
    FLY = 3


class Unit:
    def __init__(
            self, 
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
            ability_range
            ) -> None:
        
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
        self.__location = None
        self.__dead = False
        self.__player = None
        
        
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

    def special_ability(self, target, spaces):
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

    def find_move_spaces(self, i: int, j: int, range: int, space_list: list) -> set:
        valid_spaces = set()
        # Add this space if its empty, or it is this units current location
        if space_list[i][j].get_unit() == None or space_list[i][j].get_unit() == self:
            valid_spaces = {(i,j)}
        if range <= 0:
            return valid_spaces
        valid_spaces = valid_spaces.union(self.check_move_spaces(i-1, j, range, space_list))
        #valid_spaces = valid_spaces.union(self.check_move_spaces(i-1, j-1, range, space_list))
        valid_spaces = valid_spaces.union(self.check_move_spaces(i, j-1, range, space_list))
        #valid_spaces = valid_spaces.union(self.check_move_spaces(i+1, j-1, range, space_list))
        valid_spaces = valid_spaces.union(self.check_move_spaces(i+1, j, range, space_list))
        #valid_spaces = valid_spaces.union(self.check_move_spaces(i+1, j+1, range, space_list))
        valid_spaces = valid_spaces.union(self.check_move_spaces(i, j+1, range, space_list))
        #valid_spaces = valid_spaces.union(self.check_move_spaces(i-1, j+1, range, space_list))
        return valid_spaces

    def check_move_spaces(self, i: int, j: int, range: int, space_list: list) -> set:
        valid_spaces = set()
        if i >= 0 and i < BOARD_ROWS and j >= 0 and j < BOARD_COLS:
            if space_list[i][j].get_unit() != None:
                if self.__move_type != MoveType.FLY:
                    return valid_spaces
            valid_spaces = valid_spaces.union(self.find_move_spaces(i, j, range-1, space_list))
        return valid_spaces

    def find_attack_spaces(self, i: int, j: int, range: int, space_list: list) -> set:
        target_spaces = set()
        # Only add this space if there is an enemy here
        if space_list[i][j].get_unit() != None:
            if space_list[i][j].get_unit().get_player() != self.get_player():
                target_spaces = {(i,j)}
        if range <= 0:
            return target_spaces
        target_spaces = target_spaces.union(self.check_attack_spaces(i-1, j, range, space_list))
        #target_spaces = target_spaces.union(self.check_attack_spaces(i-1, j-1, range, space_list))
        target_spaces = target_spaces.union(self.check_attack_spaces(i, j-1, range, space_list))
        #target_spaces = target_spaces.union(self.check_attack_spaces(i+1, j-1, range, space_list))
        target_spaces = target_spaces.union(self.check_attack_spaces(i+1, j, range, space_list))
        #target_spaces = target_spaces.union(self.check_attack_spaces(i+1, j+1, range, space_list))
        target_spaces = target_spaces.union(self.check_attack_spaces(i, j+1, range, space_list))
        #target_spaces = target_spaces.union(self.check_attack_spaces(i-1, j+1, range, space_list))
        return target_spaces

    def check_attack_spaces(self, i: int, j: int, range: int, space_list: list) -> set:
        valid_spaces = set()
        if i >= 0 and i < BOARD_ROWS and j >= 0 and j < BOARD_COLS:
            valid_spaces = valid_spaces.union(self.find_attack_spaces(i, j, range-1, space_list))
        return valid_spaces
    
    def find_target_spaces(self, i: int, j: int, range: int, space_list: list) -> set:
        target_spaces = set()
        # Only add this space if there is an enemy here
        if space_list[i][j].get_unit() != None:
            if space_list[i][j].get_unit().get_player() != self.get_player():
                target_spaces = {(i,j)}
        if range <= 0:
            return target_spaces
        target_spaces = target_spaces.union(self.check_target_spaces(i-1, j, range, space_list))
        #target_spaces = target_spaces.union(self.check_target_spaces(i-1, j-1, range, space_list))
        target_spaces = target_spaces.union(self.check_target_spaces(i, j-1, range, space_list))
        #target_spaces = target_spaces.union(self.check_target_spaces(i+1, j-1, range, space_list))
        target_spaces = target_spaces.union(self.check_target_spaces(i+1, j, range, space_list))
        #target_spaces = target_spaces.union(self.check_target_spaces(i+1, j+1, range, space_list))
        target_spaces = target_spaces.union(self.check_target_spaces(i, j+1, range, space_list))
        #target_spaces = target_spaces.union(self.check_target_spaces(i-1, j+1, range, space_list))
        return target_spaces

    def check_target_spaces(self, i: int, j: int, range: int, space_list: list) -> set:
        valid_spaces = set()
        if i >= 0 and i < BOARD_ROWS and j >= 0 and j < BOARD_COLS:
            valid_spaces = valid_spaces.union(self.find_target_spaces(i, j, range-1, space_list))
        return valid_spaces

class Peasant(Unit):
    def __init__(self) -> None:
        hp=11
        dam_val=6
        dam_type=DamageType.BLUDGEON
        arm_val=2
        arm_type=ArmourType.PADDED
        move=MoveSpeed.MED
        move_type = MoveType.FOOT
        sprite = SpriteType.PEASANT
        name_list = Names.Commoner
        title_list = Titles.Peasant
        ability_name = "Surge of Bravery"
        ability_range = 0
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list, ability_name, ability_range)
        self.ability_used = False

class Soldier(Unit):
    def __init__(self) -> None:
        hp=16
        dam_val=8
        dam_type=DamageType.PIERCE
        arm_val=3
        arm_type=ArmourType.CHAIN
        move=MoveSpeed.MED
        move_type = MoveType.FOOT
        sprite = SpriteType.SOLDIER
        name_list = Names.Commoner
        title_list = Titles.Soldier
        ability_name = "Guarded Advance" 
        ability_range = 1        
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list, ability_name, ability_range)

    def find_target_spaces(self, i: int, j: int, range: int, space_list: list) -> set:
        target_spaces = set()
        # Only add this space if there an ally here
        if space_list[i][j].get_unit() != None:
            if space_list[i][j].get_unit().get_player() == self.get_player():
                if space_list[i][j].get_unit() != self:
                    target_spaces = {(i,j)}
        if range <= 0:
            return target_spaces
        target_spaces = target_spaces.union(self.check_target_spaces(i-1, j, range, space_list))
        #target_spaces = target_spaces.union(self.check_target_spaces(i-1, j-1, range, space_list))
        target_spaces = target_spaces.union(self.check_target_spaces(i, j-1, range, space_list))
        #target_spaces = target_spaces.union(self.check_target_spaces(i+1, j-1, range, space_list))
        target_spaces = target_spaces.union(self.check_target_spaces(i+1, j, range, space_list))
        #target_spaces = target_spaces.union(self.check_target_spaces(i+1, j+1, range, space_list))
        target_spaces = target_spaces.union(self.check_target_spaces(i, j+1, range, space_list))
        #target_spaces = target_spaces.union(self.check_target_spaces(i-1, j+1, range, space_list))
        return target_spaces

class Sorcerer(Unit):
    def __init__(self) -> None:
        hp=14
        dam_val=6
        dam_type=DamageType.PIERCE
        arm_val=1
        arm_type=ArmourType.ROBES
        move=MoveSpeed.MED
        move_type = MoveType.FOOT
        sprite = SpriteType.SORCERER
        name_list = Names.Mage
        title_list = Titles.Sorcerer
        ability_name = "Sorcerous Assault"    
        ability_range = 4    
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list, ability_name, ability_range)
        self.__special_damage = 5
        self.__special_damage_type = DamageType.MAGIC

    def special_ability(self, target, spaces):
        target_row = target.get_location().get_row()
        target_col = target.get_location().get_col()
        attack_log = []
        if target_col - 1 >= 0:
            left_target = spaces[target_row][target_col - 1].get_unit()
            if left_target != None:
                attack_log += (self.magic_attack(left_target))
        attack_log += (self.magic_attack(target))
        if target_col + 1 < BOARD_COLS:
            right_target = spaces[target_row][target_col + 1].get_unit()
            if right_target != None:
                attack_log += (self.magic_attack(right_target))
        return attack_log
        
    def magic_attack(self, target):
        unit_name = self.get_name()
        target_name = target.get_name()
        attack_log = []
        first_strike_attack = ceil(self.__special_damage * FIRST_STRIKE_BOOST)
        target_hp = target.get_curr_hp()
        self.attack(target, first_strike_attack, self.__special_damage_type)
        damage_dealt = target_hp - target.get_curr_hp()
        attack_log.append(f"{unit_name} blasts {target_name} with arcane energy, dealing {damage_dealt} damage!\n")
        if target.is_dead():
            attack_log.append(f"{unit_name} has slain {target_name}!\n")
            target.get_location().assign_unit(None)
        return attack_log

class Healer(Unit):
    def __init__(self) -> None:
        hp=15
        dam_val=8
        dam_type=DamageType.BLUDGEON
        arm_val=3
        arm_type=ArmourType.CHAIN
        move=MoveSpeed.MED
        move_type = MoveType.FOOT
        sprite = SpriteType.HEALER
        name_list = Names.Mage
        title_list = Titles.Healer
        ability_name = "Healing Radiance"
        ability_range = 1
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list, ability_name, ability_range)

    def find_target_spaces(self, i: int, j: int, range: int, space_list: list) -> set:
        target_spaces = set()
        # Only add this space if there an ally here
        if space_list[i][j].get_unit() != None:
            if space_list[i][j].get_unit().get_player() == self.get_player():
                if space_list[i][j].get_unit() != self:
                    target_spaces = {(i,j)}
        if range <= 0:
            return target_spaces
        target_spaces = target_spaces.union(self.check_target_spaces(i-1, j, range, space_list))
        #target_spaces = target_spaces.union(self.check_target_spaces(i-1, j-1, range, space_list))
        target_spaces = target_spaces.union(self.check_target_spaces(i, j-1, range, space_list))
        #target_spaces = target_spaces.union(self.check_target_spaces(i+1, j-1, range, space_list))
        target_spaces = target_spaces.union(self.check_target_spaces(i+1, j, range, space_list))
        #target_spaces = target_spaces.union(self.check_target_spaces(i+1, j+1, range, space_list))
        target_spaces = target_spaces.union(self.check_target_spaces(i, j+1, range, space_list))
        #target_spaces = target_spaces.union(self.check_target_spaces(i-1, j+1, range, space_list))
        return target_spaces

class Archer(Unit):
    def __init__(self) -> None:
        hp=15
        dam_val=6
        dam_type=DamageType.PIERCE
        arm_val=2
        arm_type=ArmourType.PADDED
        move=MoveSpeed.MED
        move_type = MoveType.FOOT
        sprite = SpriteType.ARCHER
        name_list = Names.Commoner
        title_list = Titles.Archer
        ability_name = "Ranged Attack"
        ability_range = 5
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list, ability_name, ability_range)
        self.__special_damage = 7
        self.__special_damage_type = DamageType.PIERCE

    def special_ability(self, target, spaces):
        unit_name = self.get_name()
        target_name = target.get_name()
        attack_log = []
        first_strike_attack = ceil(self.__special_damage * FIRST_STRIKE_BOOST)
        target_hp = target.get_curr_hp()
        self.attack(target, first_strike_attack, self.__special_damage_type)
        damage_dealt = target_hp - target.get_curr_hp()
        attack_log.append(f"{unit_name} fires an arrow at {target_name}, dealing {damage_dealt} damage!\n")
        if target.is_dead():
            attack_log.append(f"{unit_name} has slain {target_name}!\n")
            target.get_location().assign_unit(None)
        return attack_log

class Cavalry(Unit):
    def __init__(self) -> None:
        hp=20
        dam_val=9
        dam_type=DamageType.SLASH
        arm_val=4
        arm_type=ArmourType.PLATE
        move=MoveSpeed.FAST
        move_type = MoveType.HORSE
        sprite = SpriteType.PEASANT
        name_list = Names.Noble
        title_list = Titles.Cavalry
        ability_name = "Harrying Strike"
        ability_range = 1
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list, ability_name, ability_range)
    
    def check_move_spaces(self, i: int, j: int, range: int, space_list: list) -> set:
        valid_spaces = set()
        if i >= 0 and i < BOARD_ROWS and j >= 0 and j < BOARD_COLS:
            # If there is a solder in the space which doesn't belong to this player, return
            if isinstance(space_list[i][j].get_unit(), Soldier): 
                    if space_list[i][j].get_unit().get_player() != self.get_player():
                        return valid_spaces 
            # Otherwise proceed
            valid_spaces = valid_spaces.union(self.find_move_spaces(i, j, range-1, space_list))
        return valid_spaces
    

class Archmage(Unit):
    def __init__(self) -> None:
        hp=22
        dam_val=7
        dam_type=DamageType.BLUDGEON
        arm_val=1
        arm_type=ArmourType.ROBES
        move=MoveSpeed.MED
        move_type = MoveType.FLY
        sprite = SpriteType.ARCHMAGE
        name_list = Names.Mage
        title_list = Titles.Archmage
        ability_name = "Arcane Vortex"
        ability_range = 3
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list, ability_name, ability_range)
        self.__special_damage = 6
        self.__special_damage_type = DamageType.MAGIC

    def special_ability(self, target, spaces):
        target_row = target.get_location().get_row()
        target_col = target.get_location().get_col()
        attack_log = []
        if target_row - 1 >= 0:
            top_target = spaces[target_row - 1][target_col].get_unit()
            if top_target != None:
                attack_log += (self.magic_attack(top_target))
        if target_col - 1 >= 0:
            left_target = spaces[target_row][target_col - 1].get_unit()
            if left_target != None:
                attack_log += (self.magic_attack(left_target))
        attack_log += (self.magic_attack(target))
        if target_col + 1 < BOARD_COLS:
            right_target = spaces[target_row][target_col + 1].get_unit()
            if right_target != None:
                attack_log += (self.magic_attack(right_target))
        if target_row + 1 < BOARD_ROWS:
            bottom_target = spaces[target_row + 1][target_col].get_unit()
            if bottom_target != None:
                attack_log += (self.magic_attack(bottom_target))
        return attack_log
        
    def magic_attack(self, target):
        unit_name = self.get_name()
        target_name = target.get_name()
        attack_log = []
        first_strike_attack = ceil(self.__special_damage * FIRST_STRIKE_BOOST)
        target_hp = target.get_curr_hp()
        self.attack(target, first_strike_attack, self.__special_damage_type)
        damage_dealt = target_hp - target.get_curr_hp()
        attack_log.append(f"{unit_name} blasts {target_name} with arcane energy, dealing {damage_dealt} damage!\n")
        if target.is_dead():
            attack_log.append(f"{unit_name} has slain {target_name}!\n")
            target.get_location().assign_unit(None)
        return attack_log

class General(Unit):
    def __init__(self) -> None:
        hp=24
        dam_val=10
        dam_type=DamageType.SLASH
        arm_val=4
        arm_type=ArmourType.PLATE
        move=MoveSpeed.SLOW
        move_type = MoveType.FOOT
        sprite = SpriteType.PEASANT
        name_list = Names.Noble
        title_list = Titles.General
        ability_name = "Inspirational Rally"
        ability_range = 0
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list, ability_name, ability_range)
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
            return Effect.STRONG
        
    elif weapon == DamageType.MAGIC:
        if armour == ArmourType.ROBES:
            return Effect.POOR
        elif armour == ArmourType.PADDED:
            return Effect.NEUTRAL
        elif armour == ArmourType.CHAIN:
            return Effect.STRONG
        elif armour == ArmourType.PLATE:
            return Effect.STRONG
        
    return None
