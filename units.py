from enum import IntEnum
from math import ceil
from gameBoard import Space
from graphics import SpriteType

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
            sprite
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
    
    def get_player(self):
        return self.__player
    
    def get_sprite(self):
        return self.__sprite
    
    def set_player(self, player):
        self.__player = player

    def move(self):
        pass

    def _place(self, space: Space):
        self.location = space

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
            self.move()

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




class Peasant(Unit):
    def __init__(self, 
                 hp=9, 
                 dam_val=5, 
                 dam_type=DamageType.BLUDGEON, 
                 arm_val=2, 
                 arm_type=ArmourType.PADDED, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT,
                 sprite = SpriteType.PEASANT
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite)

class Soldier(Unit):
    def __init__(self, 
                 hp=15, 
                 dam_val=7, 
                 dam_type=DamageType.PIERCE, 
                 arm_val=3, 
                 arm_type=ArmourType.CHAIN, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT,
                 sprite = SpriteType.SOLDIER
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite)

class Sorcerer(Unit):
    def __init__(self, 
                 hp=12, 
                 dam_val=5, 
                 dam_type=DamageType.PIERCE, 
                 arm_val=1, 
                 arm_type=ArmourType.ROBES, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT,
                 sprite = SpriteType.SORCERER
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite)

class Healer(Unit):
    def __init__(self, 
                 hp=14, 
                 dam_val=7, 
                 dam_type=DamageType.BLUDGEON, 
                 arm_val=3, 
                 arm_type=ArmourType.CHAIN, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT,
                 sprite = SpriteType.PEASANT
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite)

class Archer(Unit):
    def __init__(self, 
                 hp=14, 
                 dam_val=6, 
                 dam_type=DamageType.PIERCE, 
                 arm_val=2, 
                 arm_type=ArmourType.PADDED, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT,
                 sprite = SpriteType.ARCHER
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite)

class Cavalry(Unit):
    def __init__(self, 
                 hp=18, 
                 dam_val=8, 
                 dam_type=DamageType.SLASH, 
                 arm_val=4, 
                 arm_type=ArmourType.PLATE, 
                 move=MoveSpeed.FAST, 
                 move_type = MoveType.HORSE,
                 sprite = SpriteType.PEASANT
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite)

class Archmage(Unit):
    def __init__(self, 
                 hp=20, 
                 dam_val=7, 
                 dam_type=DamageType.BLUDGEON, 
                 arm_val=1, 
                 arm_type=ArmourType.ROBES, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FLY,
                 sprite = SpriteType.PEASANT
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite)

class General(Unit):
    def __init__(self, 
                 hp=22, 
                 dam_val=10, 
                 dam_type=DamageType.SLASH, 
                 arm_val=4, 
                 arm_type=ArmourType.PLATE, 
                 move=MoveSpeed.SLOW, 
                 move_type = MoveType.FOOT,
                 sprite = SpriteType.PEASANT
                 ) -> None:
        super().__init__(hp, dam_val, dam_type, arm_val, arm_type, move, move_type, sprite)


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
