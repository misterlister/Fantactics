from enum import IntEnum
from math import ceil
from gameBoard import Space
from graphics import SpriteType
from random import randint
from names import Names, Titles

FIRST_STRIKE_BOOST = 1.2
POOR_EFFECT_MOD = 3/4
STRONG_EFFECT_MOD = 4/3

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
    SLOW = 1
    MED = 2
    FAST = 3

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
            title_list
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
    
    def set_player(self, player):
        self.__player = player

    def make_name(self, names: list, titles: list) -> str:
        name_index = randint(0, len(names)-1)
        title_index = randint(0, len(titles)-1)
        name = f"{names[name_index]} the {titles[title_index]}"
        return name

    def move(self, space: Space):
        try:
            if space.contains() is None:
                self.__location.assign_unit(None)
                self.__location = space
                space.assign_unit(self)
            else:
                raise Exception("Error: Cannot move unit into another unit's space")
        except Exception as e:
            return e
        
    def _place(self, space: Space):
        self.__location = space

    def take_damage(self, damage):
        self.__curr_hp -= damage
        if self.__curr_hp <= 0:
            self.die()

    def heal(self, healing):
        if healing + self.__curr_hp > self.__max_hp:
            self.__curr_hp = self.__max_hp
        else:
            self.__curr_hp += healing

    def is_dead(self):
        if self.__dead:
            return True
        return False

    def basic_attack(self, target):
        first_strike_attack = ceil(self.__damage * FIRST_STRIKE_BOOST)
        self.attack(target, first_strike_attack, self.__damage_type)
        if target.is_dead():
            #self.move()
            pass

    def retaliate(self, target):
        self.attack(target, self.__damage, self.__damage_type)

    def attack(self, target, damage: int, damage_type):
        effectiveness = weapon_matchup(damage_type, target.get_armour_type())
        atk_damage = damage
        if effectiveness == Effect.STRONG:
            atk_damage = ceil(atk_damage * STRONG_EFFECT_MOD)
        atk_damage -= target.get_armour_val()
        if effectiveness == Effect.POOR:
            atk_damage = ceil(atk_damage * POOR_EFFECT_MOD)
        target.take_damage(atk_damage)

    def special_ability(self):
        pass

    def die(self):
        self.__dead = True

    def choose_action(self):
        print("Choose Action!")


class Peasant(Unit):
    def __init__(self, 
                 hp=9, 
                 dam_val=5, 
                 dam_type=DamageType.BLUDGEON, 
                 arm_val=2, 
                 arm_type=ArmourType.PADDED, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT,
                 sprite = SpriteType.PEASANT,
                 name_list = Names.COMMONER,
                 title_list = Titles.PEASANT
                 ) -> None:
        
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list)

class Soldier(Unit):
    def __init__(self, 
                 hp=15, 
                 dam_val=7, 
                 dam_type=DamageType.PIERCE, 
                 arm_val=3, 
                 arm_type=ArmourType.CHAIN, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT,
                 sprite = SpriteType.SOLDIER,
                 name_list = Names.COMMONER,
                 title_list = Titles.SOLDIER
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list)

class Sorcerer(Unit):
    def __init__(self, 
                 hp=12, 
                 dam_val=5, 
                 dam_type=DamageType.PIERCE, 
                 arm_val=1, 
                 arm_type=ArmourType.ROBES, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT,
                 sprite = SpriteType.SORCERER,
                 name_list = Names.MAGE,
                 title_list = Titles.SORCERER
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list)

class Healer(Unit):
    def __init__(self, 
                 hp=14, 
                 dam_val=7, 
                 dam_type=DamageType.BLUDGEON, 
                 arm_val=3, 
                 arm_type=ArmourType.CHAIN, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT,
                 sprite = SpriteType.PEASANT,
                 name_list = Names.MAGE,
                 title_list = Titles.HEALER
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list)

class Archer(Unit):
    def __init__(self, 
                 hp=14, 
                 dam_val=6, 
                 dam_type=DamageType.PIERCE, 
                 arm_val=2, 
                 arm_type=ArmourType.PADDED, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT,
                 sprite = SpriteType.ARCHER,
                 name_list = Names.COMMONER,
                 title_list = Titles.ARCHER
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list)

class Cavalry(Unit):
    def __init__(self, 
                 hp=18, 
                 dam_val=8, 
                 dam_type=DamageType.SLASH, 
                 arm_val=4, 
                 arm_type=ArmourType.PLATE, 
                 move=MoveSpeed.FAST, 
                 move_type = MoveType.HORSE,
                 sprite = SpriteType.PEASANT,
                 name_list = Names.NOBLE,
                 title_list = Titles.CAVALRY
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list)

class Archmage(Unit):
    def __init__(self, 
                 hp=20, 
                 dam_val=7, 
                 dam_type=DamageType.BLUDGEON, 
                 arm_val=1, 
                 arm_type=ArmourType.ROBES, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FLY,
                 sprite = SpriteType.PEASANT,
                 name_list = Names.MAGE,
                 title_list = Titles.ARCHMAGE
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list)

class General(Unit):
    def __init__(self, 
                 hp=22, 
                 dam_val=10, 
                 dam_type=DamageType.SLASH, 
                 arm_val=4, 
                 arm_type=ArmourType.PLATE, 
                 move=MoveSpeed.SLOW, 
                 move_type = MoveType.FOOT,
                 sprite = SpriteType.PEASANT,
                 name_list = Names.NOBLE,
                 title_list = Titles.GENERAL
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite, name_list, title_list)


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
