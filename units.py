from enum import IntEnum


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

class MoveSpeed(IntEnum):
    SLOW = 1
    MED = 2
    FAST = 3

class MoveType(IntEnum):
    FOOT = 1
    HORSE = 2
    FLY = 3


class Unit:
    def __init__(self, location, hp, dam_val, dam_type, arm_val, arm_type, move, move_type) -> None:
        self.location = location
        self.max_hp = hp
        self.curr_hp = hp
        self.damage = dam_val
        self.damage_type = dam_type
        self.armour = arm_val
        self.armour_type = arm_type
        self.movement = move
        self.move_type = move_type
        

    def move(self):
        pass

    def attack(self, target):
        pass

    def special_ability(self):
        pass

    def take_damage(self, damage):
        pass

    def heal(self, healing):
        pass

    def get_max_hp(self):
        pass

    def get_curr_hp(self):
        pass

class Peasant(Unit):
    def __init__(self, 
                 location, 
                 hp=10, 
                 dam_val=7, 
                 dam_type=DamageType.BLUDGEON, 
                 arm_val=2, 
                 arm_type=ArmourType.PADDED, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT
                 ) -> None:
        super().__init__(hp, location, dam_val, dam_type, arm_val, arm_type, move, move_type)

class Soldier(Unit):
    def __init__(self, 
                 location, 
                 hp=15, 
                 dam_val=9, 
                 dam_type=DamageType.PIERCE, 
                 arm_val=3, 
                 arm_type=ArmourType.CHAIN, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT
                 ) -> None:
        super().__init__(hp, location, dam_val, dam_type, arm_val, arm_type, move, move_type)

class Sorcerer(Unit):
    def __init__(self, 
                 location, 
                 hp=12, 
                 dam_val=6, 
                 dam_type=DamageType.PIERCE, 
                 arm_val=1, 
                 arm_type=ArmourType.ROBES, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT
                 ) -> None:
        super().__init__(hp, location, dam_val, dam_type, arm_val, arm_type, move, move_type)

class Healer(Unit):
    def __init__(self, 
                 location, 
                 hp=14, 
                 dam_val=8, 
                 dam_type=DamageType.BLUDGEON, 
                 arm_val=3, 
                 arm_type=ArmourType.CHAIN, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT
                 ) -> None:
        super().__init__(hp, location, dam_val, dam_type, arm_val, arm_type, move, move_type)

class Archer(Unit):
    def __init__(self, 
                 location, 
                 hp=14, 
                 dam_val=7, 
                 dam_type=DamageType.PIERCE, 
                 arm_val=2, 
                 arm_type=ArmourType.PADDED, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FOOT
                 ) -> None:
        super().__init__(hp, location, dam_val, dam_type, arm_val, arm_type, move, move_type)

class Cavalry(Unit):
    def __init__(self, 
                 location, 
                 hp=18, 
                 dam_val=10, 
                 dam_type=DamageType.SLASH, 
                 arm_val=4, 
                 arm_type=ArmourType.PLATE, 
                 move=MoveSpeed.FAST, 
                 move_type = MoveType.HORSE
                 ) -> None:
        super().__init__(hp, location, dam_val, dam_type, arm_val, arm_type, move, move_type)

class Archmage(Unit):
    def __init__(self, 
                 location, 
                 hp=20, 
                 dam_val=9, 
                 dam_type=DamageType.BLUDGEON, 
                 arm_val=1, 
                 arm_type=ArmourType.ROBES, 
                 move=MoveSpeed.MED, 
                 move_type = MoveType.FLY
                 ) -> None:
        super().__init__(hp, location, dam_val, dam_type, arm_val, arm_type, move, move_type)

class General(Unit):
    def __init__(self, 
                 location, 
                 hp=22, 
                 dam_val=11, 
                 dam_type=DamageType.SLASH, 
                 arm_val=4, 
                 arm_type=ArmourType.PLATE, 
                 move=MoveSpeed.SLOW, 
                 move_type = MoveType.FOOT
                 ) -> None:
        super().__init__(hp, location, dam_val, dam_type, arm_val, arm_type, move, move_type)