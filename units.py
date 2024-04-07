from math import ceil
from graphics import SpriteType
from random import randint
from names import Names, Titles
from constants import *
from space import Space

class Unit:
    def __init__(
            self, 
            unit_type: str,
            hp: int, 
            dam_val: int, 
            dam_type: DamageType, 
            def_val: int, 
            arm_type: ArmourType, 
            move: MoveSpeed, 
            move_type: MoveType,
            sprite,
            name_list,
            title_list,
            ability_name,
            ability_range,
            ability_min_range,
            ability_value
            ) -> None:
        
        self.__unit_type = unit_type
        self.__max_hp = hp
        self.__curr_hp = hp
        self.__damage = dam_val
        self.__damage_type = dam_type
        self.__defense = def_val
        self.__armour_type = arm_type
        self.__movement = move
        self.__move_type = move_type
        self.__sprite = sprite
        self.__name = self.make_name(name_list, title_list)
        self.__ability_name = ability_name
        self.__ability_range = ability_range
        self.__ability_min_range = ability_min_range
        self.__ability_value = ability_value
        self.__ability_disabled_duration = 0
        self.__ability_used = False
        self.__space = None # Space where a unit currently is
        self.__action_space = None # Space where a unit is currently acting from
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
    
    def get_defense_val(self):
        return self.__defense
    
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
    
    def get_space(self):
        return self.__space
    
    def get_action_space(self):
        return self.__action_space
    
    def get_ability_name(self):
        return self.__ability_name
    
    def get_ability_range(self):
        return self.__ability_range
    
    def get_ability_min_range(self):
        return self.__ability_min_range
    
    def get_ability_value(self):
        return self.__ability_value
    
    def get_ability_targets(self):
        return self.__ability_targets
    
    def get_damage_mod(self):
        mod_total = 0
        mod_total += get_aura_damage_mods(self)
        if mod_total < 0:
            mod_total = 0
        return mod_total
    
    def get_defense_mod(self):
        mod_total = 0
        mod_total += get_aura_defense_mods(self)
        mod_total += self.__action_space.get_defense_mod()
        return mod_total
    
    def expend_ability(self):
        self.__ability_used = True
    
    def ability_expended(self):
        return self.__ability_used
    
    def disable_ability(self, duration: int):
        self.__ability_disabled_duration = duration
        
    def decrement_disabled_counter(self):
        self.__ability_disabled_duration -= 1
        
    def get_disabled_message(self):
        return f"{self.get_name()} cannot use their ability for {self.__ability_disabled_duration} turns."
    
    def ability_disabled(self):
        if self.__ability_disabled_duration > 0:
                return True
        return False
    
    def set_name(self, name):
        self.__name = name
    
    def set_action_space(self, space):
        self.__action_space = space
        
    def reset_action_space(self):
        self.__action_space = self.__space
    
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

    def move(self, space):
        old_space = self.get_space()
        move_log = []
        if old_space != space:
            try:
                if space.get_unit() == None:
                    # Remove the unit from their previous space (Unless they are swapping with a Soldier)
                    if self.__space.get_unit() == self:
                        self.__space.assign_unit(None)
                    self.__space = space
                    self.__action_space = space
                    space.assign_unit(self)
                    move_log.append(f"{self.get_name()} -> {chr(space.get_col() + 65)} {space.get_row() + 1}.\n")
                else:
                    raise Exception("Error: Cannot move unit into another unit's space")
            except Exception as e:
                print(e)
        else:
            move_log.append(f"{self.get_name()} stayed in place.\n")
        return move_log
        
    def _place(self, space):
        self.__space = space
        self.__action_space = space

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
    
    def first_strike_damage(self):
        damage = self.__damage + self.get_damage_mod()
        return ceil(damage * FIRST_STRIKE_BOOST)

    def basic_attack(self, target):
        first_strike_attack = self.first_strike_damage()
        self_name = self.get_name()
        target_name = target.get_name()
        self_loc = self.get_space()
        target_loc = target.get_space()
        attack_log = []
        target_hp = target.get_curr_hp()
        self.attack(target, first_strike_attack, self.__damage_type)
        damage_dealt = target_hp - target.get_curr_hp()
        attack_log.append(f"{self_name} attacks {target_name}, dealing {damage_dealt} damage!\n")
        if target.is_dead(): # If the target is dead, remove them and take their place
            attack_log.append(f"{self_name} has slain {target_name}!\n")
            target_loc.assign_unit(None)
            self.move(target_loc)
        else: # Otherwise, they will retaliate
            attack_log.append(target.retaliate(self))
            if self.is_dead(): # If the unit died, remove them
                attack_log.append(f"{self_name} has been slain by {target_name}!\n")
                self_loc.assign_unit(None)
        return attack_log
    
    def attack_preview(self, target, first_strike = False):
        if first_strike:
            attack_damage = self.first_strike_damage()
        else:
            attack_damage = self.__damage + self.get_damage_mod()
        damage_dealt = self.calculate_damage(target, attack_damage, self.__damage_type)
        return damage_dealt

    def ability_preview(self, target):
        return None, None

    def retaliate(self, target):
        target_hp = target.get_curr_hp()
        damage = self.__damage + self.get_damage_mod()
        self.attack(target, damage, self.__damage_type)
        damage_dealt = target_hp - target.get_curr_hp()
        retaliation_log = f"{self.get_name()} retaliates against {target.get_name()}, dealing {damage_dealt} damage!\n"
        return retaliation_log

    def attack(self, target, damage: int, damage_type):
        atk_damage = self.calculate_damage(target, damage, damage_type)
        target.take_damage(atk_damage)

    def calculate_damage(self, target, damage, damage_type) -> int:
        effectiveness = weapon_matchup(damage_type, target.get_armour_type())
        atk_damage = damage
        if effectiveness == Effect.STRONG:
            atk_damage = ceil(atk_damage * STRONG_EFFECT_MOD)
        target_defense = target.get_defense_val() + target.get_defense_mod()
        atk_damage -= target_defense
        if effectiveness == Effect.POOR:
            atk_damage = ceil(atk_damage * POOR_EFFECT_MOD)
        return atk_damage

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
    
    def find_target_spaces(self, space, range: int, target_dict: dict, action = None, pass_dict: dict = TARGET_ALL) -> set:
        # Add this space if it is a valid target
        target_spaces = set()
        if range < 0:
            return target_spaces
        if self.verify_target(space, target_dict):
            target_spaces = {space}
        if range == 0:
            return target_spaces
        target_spaces = target_spaces.union(self.check_target_spaces(space.get_left(), range, target_dict, action, pass_dict))
        target_spaces = target_spaces.union(self.check_target_spaces(space.get_up(), range, target_dict, action, pass_dict))
        target_spaces = target_spaces.union(self.check_target_spaces(space.get_right(), range, target_dict, action, pass_dict))
        target_spaces = target_spaces.union(self.check_target_spaces(space.get_down(), range, target_dict, action, pass_dict))
        return target_spaces
    
    def check_target_spaces(self, space, range: int, target_dict: dict, action, pass_dict: dict) -> set:
        valid_spaces = set()
        if space != None: # If this space doesn't exist, return
            if self.verify_space_pass(space, pass_dict, action):
                move_cost = 1
                # If this is a move action, determine the move cost of the terrain
                if action == ActionType.MOVE:
                    # Flying units ignore terrain
                    if self.get_move_type() != MoveType.FLY:
                        move_cost = space.get_move_cost()
                        # If this unit is riding a horse, increase difficult terrain movement cost
                        if self.get_move_type() == MoveType.HORSE:
                            if move_cost > 1:
                                move_cost = move_cost * 2
                valid_spaces = valid_spaces.union(self.find_target_spaces(space, (range - move_cost), target_dict, action, pass_dict))
        return valid_spaces
    
    def verify_space_pass(self, space, target_dict, action) -> bool:
        if action == ActionType.MOVE:
            unit = space.get_unit()
            if unit != None:
                if unit.get_move_type() == MoveType.FLY:
                    return True
        return self.verify_target(space, target_dict)
    
    def verify_target(self, space, target_dict: dict) -> bool:
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
    
    def adjacent_to(self, unit_type, ally: bool, range: int = 1) -> bool:
        space = self.get_action_space()
        if ally:
            include = TARGET_ALLIES
        else:
            include = TARGET_ENEMIES
        spaces = self.find_target_spaces(space, range, include)
        for space in spaces:
            try:
                if space.get_unit().is_unit_type(unit_type):
                    return True
            except Exception as e:
                print(e)
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
        def_val=0
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
        ability_range = 1
        ability_min_range = 0
        ability_value = 1
        super().__init__(unit_type, hp, dam_val, dam_type, def_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_min_range, ability_value)
        self.set_ability_targets(TARGET_SELF_ENEMIES)
        self.__brave = False
        
    def special_ability(self, target: Unit, space: Space):
        self.expend_ability()
        unit_name = self.get_name()
        attack_log = []
        self.__brave = True
        self.get_player().add_effected_unit(self)
        attack_log.append(f"{unit_name} has a {self.get_ability_name()}! They have temporarily unlocked unexpected strength.\n")
        if target != self:
            attack_log.extend(self.basic_attack(target))
        return attack_log
    
    def get_damage_mod(self):
        mod_total = 0
        mod_total += get_aura_damage_mods(self)
        mod_total += self.bravery_mod()
        if mod_total < 0:
            mod_total = 0
        return mod_total
    
    def get_defense_mod(self):
        mod_total = 0
        mod_total += get_aura_defense_mods(self)
        mod_total += self.get_action_space().get_defense_mod()
        mod_total += self.bravery_mod()
        if mod_total < 0:
            mod_total = 0
        return mod_total

    def is_brave(self):
        return self.__brave 
    
    def end_brave(self):
        self.__brave = False
        
    def bravery_mod(self):
        if self.is_brave():
            return self.get_ability_value()
        return 0
    
    def ability_preview(self, target: Unit):
        if target == None:
            return None, None
        self.__brave = True
        damage_dealt = self.attack_preview(target, True)
        if damage_dealt >= target.get_curr_hp():
            damage_received = 0
        else:
            damage_received = target.attack_preview(self, False)
        self.__brave = False
        return damage_dealt, damage_received
    
    def move(self, space):
        move_log = super().move(space)
        row = self.get_space().get_row()
        team = self.get_player().get_team_colour()
        if ((row == 0 and team == "white")
            or (row == BOARD_ROWS -1 and team == "black")):
            move_log.append(self.promotion())
        return move_log
    
    def promotion(self):
        player = self.get_player()
        new_unit = player.get_state().promote_unit(self)
        before_name = self.get_name()
        name = before_name.split()[0]
        damage = self.get_max_hp() - self.get_curr_hp()
        space = self.get_space()
        space.assign_unit(new_unit)
        new_unit._place(space)
        title = " ".join(new_unit.get_name().split()[1:])
        after_name = name + " " + title
        new_unit.set_name(after_name)
        new_unit.take_damage(damage)
        player.remove_unit(self)
        player.assign_unit(new_unit)
        return f"{before_name} has been promoted to {after_name}!\n"


class Soldier(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "Soldier"
        hp=16
        dam_val=6
        dam_type=DamageType.PIERCE
        def_val=0#1
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
        ability_min_range = 1
        ability_value = None
        super().__init__(unit_type, hp, dam_val, dam_type, def_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_min_range, ability_value)
        self.set_ability_targets(TARGET_ALLIES)

    def special_ability(self, target: Unit, space: Space):
        unit_name = self.get_name()
        target_name = target.get_name()
        ability_log = []
        current_space = self.get_space()
        current_space.assign_unit(None)
        ability_log.append(f"{unit_name} makes a {self.get_ability_name()}, moving to defend {target_name} and taking their place.\n")
        target.move(current_space)
        self.move(space)
        return ability_log

class Archer(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "Archer"
        hp=15
        dam_val=5
        dam_type=DamageType.PIERCE
        def_val=0
        arm_type=ArmourType.PADDED
        move=MoveSpeed.MED
        move_type = MoveType.FOOT
        if p1:
            sprite = SpriteType.ARCHER1
        else:
            sprite = SpriteType.ARCHER2
        name_list = Names.Commoner
        title_list = Titles.Archer
        ability_name = "Arrow Volley"
        ability_range = 5
        ability_min_range = 2
        ability_value = 8
        super().__init__(unit_type, hp, dam_val, dam_type, def_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_min_range, ability_value)
        self.set_ability_targets(TARGET_ENEMIES)
        self.__special_damage_type = DamageType.PIERCE

    def special_ability(self, target: Unit, space: Space):
        unit_name = self.get_name()
        target_name = target.get_name()
        attack_log = []
        attack_damage = self.get_ability_value() + self.get_damage_mod()
        target_hp = target.get_curr_hp()
        self.attack(target, attack_damage, self.__special_damage_type)
        damage_dealt = target_hp - target.get_curr_hp()
        attack_log.append(f"{unit_name} fires an {self.get_ability_name()} at {target_name}, dealing {damage_dealt} damage!\n")
        if target.is_dead():
            attack_log.append(f"{unit_name} has slain {target_name}!\n")
            target.get_space().assign_unit(None)
        return attack_log
    
    def ability_preview(self, target: Unit):
        if target == None:
            return None, None
        damage = self.get_ability_value() + self.get_damage_mod()
        damage_dealt = self.calculate_damage(target, damage, self.__special_damage_type)
        return damage_dealt, 0
    
    def get_damage_mod(self):
        damage_mod = super().get_damage_mod()
        damage_mod += self.get_action_space().get_defense_mod()
        return damage_mod
    
    # Variation of defense calculation that doubles terrain bonuses
    def get_defense_mod(self):
        defense_mod =  super().get_defense_mod()
        defense_mod += self.get_action_space().get_defense_mod()
        return defense_mod

class Cavalry(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "Cavalry"
        hp=18
        dam_val=7
        dam_type=DamageType.SLASH
        def_val=0#1
        arm_type=ArmourType.PLATE
        move=MoveSpeed.FAST
        move_type = MoveType.HORSE
        if p1:
            sprite = SpriteType.CAVALRY1
        else:
            sprite = SpriteType.CAVALRY2
        name_list = Names.Noble
        title_list = Titles.Cavalry
        ability_name = "Harrying Strike"
        ability_range = 1
        ability_min_range = 0
        ability_value = 6
        super().__init__(unit_type, hp, dam_val, dam_type, def_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_min_range, ability_value)
        self.set_ability_targets(TARGET_ENEMIES)
        self.__ability_duration = 2
    
    # Variation of movement verification that can pass all units except Enemy-aligned Soldiers
    def verify_space_pass(self, space: Space, target_dict, action) -> bool:
        if action == ActionType.MOVE:
            unit = space.get_unit()
            if unit != None:
                if not self.is_ally(unit):
                    if isinstance(unit, Soldier):
                        return False
            return True
        else:
            return self.verify_target(space, target_dict)
    
    def special_ability(self, target: Unit, space: Space):    
        ability_damage = self.get_ability_value()
        self_name = self.get_name()
        target_name = target.get_name()
        self_loc = self.get_space()
        target_loc = target.get_space()
        attack_log = []
        target_hp = target.get_curr_hp()
        self.attack(target, ability_damage, self.get_damage_type())
        damage_dealt = target_hp - target.get_curr_hp()
        attack_log.append(f"{self_name} unleashes a {self.get_ability_name()} at {target_name}, dealing {damage_dealt} damage!\n")
        if target.is_dead(): # If the target is dead, remove them and take their place
            attack_log.append(f"{self_name} has slain {target_name}!\n")
            target_loc.assign_unit(None)
            self.move(target_loc)
        else: # Otherwise, they will retaliate
            attack_log.append(target.retaliate(self))
            if self.is_dead(): # If the unit died, remove them
                attack_log.append(f"{self_name} has been slain by {target_name}!\n")
                self_loc.assign_unit(None)
            attack_log.append(f"{target_name} was harried! They cannot use their ability for their next {self.__ability_duration} turns!\n")
            target.disable_ability(self.__ability_duration + 1)
            target.get_player().add_effected_unit(target)
        return attack_log
    
    def ability_preview(self, target: Unit):
        if target == None:
            return None, None
        damage = self.get_ability_value() + self.get_damage_mod()
        damage_dealt = self.calculate_damage(target, damage, self.get_damage_type())
        if damage_dealt >= target.get_curr_hp():
            damage_received = 0
        else:
            damage_received = target.attack_preview(self, False)
        return damage_dealt, damage_received
    
    
class Sorcerer(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "Sorcerer"
        hp=14
        dam_val=4
        dam_type=DamageType.PIERCE
        def_val=0
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
        ability_min_range = 0
        ability_value = 7
        super().__init__(unit_type, hp, dam_val, dam_type, def_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_min_range, ability_value)
        self.set_ability_targets(TARGET_ALL)
        self.__special_damage_type = DamageType.MAGIC
        self._ability_area_of_effect.extend([Direction.LEFT, Direction.RIGHT])
        self.__heal_value = 1
    
    def attack(self, target: Unit, damage: int, damage_type):
        self.heal(self.__heal_value)
        return super().attack(target, damage, damage_type)

    def retaliate(self, target: Unit):
        attack_log = super().retaliate(target)
        return attack_log + "\n" + self.siphon_message()
    
    def basic_attack(self, target: Unit):
        attack_log = super().basic_attack(target)
        if not self.is_dead():
            siphon = self.siphon_message()
            attack_log.append(siphon)
        return attack_log
    
    def siphon_message(self, mul = 1):
        healing = self.__heal_value * mul
        return f"{self.get_name()} heals {healing} hp by siphoning life force\n"
        
    def special_ability(self, target: Unit, space: Space):
        ability_log = [f"{self.get_name()} releases a {self.get_ability_name()}!\n"]
        attack_log = []
        siphon_targets = 0
        main_damage = self.get_ability_value() + self.get_damage_mod()
        splash_damage = ceil(main_damage/2)
        left_space = space.get_left()
        if left_space is not None:
            left_target = left_space.get_unit()
            if left_target != None:
                siphon_targets += 1
                attack_log += (self.magic_power(left_target, splash_damage))
        if target is not None:
            siphon_targets += 1
            attack_log += (self.magic_power(target, main_damage))
        right_space = space.get_right()
        if right_space is not None:
            right_target = right_space.get_unit()
            if right_target != None:
                siphon_targets += 1
                attack_log += (self.magic_power(right_target, splash_damage))
        if siphon_targets == 0:
            ability_log.append("There was no target, so it has no effect!\n")
            return ability_log
        attack_log.append(self.siphon_message(siphon_targets))
        ability_log.extend(attack_log)
        return ability_log
    
    def magic_power(self, target: Unit, damage: int):
        unit_name = self.get_name()
        if target is self:
            target_name = "themself"
        else:
            target_name = target.get_name()
        attack_log = []
        target_hp = target.get_curr_hp()
        self.attack(target, damage, self.__special_damage_type)
        damage_dealt = target_hp - target.get_curr_hp()
        attack_log.append(f"The {self.get_ability_name()} blasts {target_name}, dealing {damage_dealt} damage!\n")
        if target.is_dead():
            attack_log.append(f"{unit_name} has slain {target_name}!\n")
            target.get_space().assign_unit(None)
        return attack_log
    
    def ability_preview(self, target: Unit):
        if target == None:
            return None, None
        ability_damage = self.get_ability_value() + self.get_damage_mod()
        damage_dealt = self.calculate_damage(target, ability_damage, self.__special_damage_type)
        damage_received = 0
        self_space = self.get_action_space()
        target_space = target.get_space()
        if (target_space.get_left() == self_space
            or target_space.get_right() == self_space):
            splash_damage = ceil(ability_damage/2)
            damage_received = self.calculate_damage(self, splash_damage, self.__special_damage_type)
        elif target_space == self_space:
            damage_received = self.calculate_damage(self, ability_damage, self.__special_damage_type)
        return damage_dealt, damage_received

class Healer(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "Healer"
        hp=15
        dam_val=6
        dam_type=DamageType.BLUDGEON
        def_val=0#1
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
        ability_min_range = 0
        ability_value = 5
        super().__init__(unit_type, hp, dam_val, dam_type, def_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_min_range, ability_value)
        self.set_ability_targets(TARGET_SELF)
        self._ability_area_of_effect.extend([Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN])

    def special_ability(self, target: Unit, space: Space):
        ability_log = [f"{self.get_name()} infuses their surroundings with {self.get_ability_name()}.\n"]
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
            attack_log.append("The warmth is pleasant, but it has no effect!\n")
        ability_log.extend(attack_log)
        return ability_log
        
    def magic_power(self, target: Unit):
        if self.get_player() == target.get_player():
            target_name = target.get_name()
            attack_log = []
            target_hp = target.get_curr_hp()
            target.heal(self.get_ability_value())
            damage_healed = target.get_curr_hp() - target_hp
            if damage_healed > 0:
                attack_log.append(f"The {self.get_ability_name()} heals {target_name} for {damage_healed} hp!\n")
        return attack_log

class Archmage(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "Archmage"
        hp=22
        dam_val=5
        dam_type=DamageType.BLUDGEON
        def_val=0
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
        ability_min_range = 0
        ability_value = 8
        super().__init__(unit_type, hp, dam_val, dam_type, def_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_min_range, ability_value)
        self.set_ability_targets(TARGET_ALL)
        self.__special_damage_type = DamageType.MAGIC
        self._ability_area_of_effect.extend([Direction.UP, Direction.LEFT, Direction.RIGHT, Direction.DOWN])

    def special_ability(self, target: Unit, space: Space):
        ability_log = [f"{self.get_name()} unleashes an {self.get_ability_name()}!\n"]
        attack_log = []
        main_damage = self.get_ability_value() + self.get_damage_mod()
        splash_damage = ceil(main_damage/2)
        top_space = space.get_up()
        if top_space is not None:
            top_target = top_space.get_unit()
            if top_target is not None:
                attack_log += (self.magic_power(top_target, splash_damage))
        left_space = space.get_left()
        if left_space is not None:
            left_target = left_space.get_unit()
            if left_target is not None:
                attack_log += (self.magic_power(left_target, splash_damage))
        if target is not None:
            attack_log += (self.magic_power(target, main_damage))
        right_space = space.get_right()
        if right_space is not None:
            right_target = right_space.get_unit()
            if right_target != None:
                attack_log += (self.magic_power(right_target, splash_damage))
        down_space = space.get_down()
        if down_space is not None:
            down_target = down_space.get_unit()
            if down_target != None:
                attack_log += (self.magic_power(down_target, splash_damage))
        if len(attack_log) == 0:
            attack_log.append("There was no target, so it has no effect!\n")
        ability_log.extend(attack_log)
        return ability_log
        
    def magic_power(self, target: Unit, damage: int):
        unit_name = self.get_name()
        if target is self:
            target_name = "themself"
        else:
            target_name = target.get_name()
        attack_log = []
        target_hp = target.get_curr_hp()
        self.attack(target, damage, self.__special_damage_type)
        damage_dealt = target_hp - target.get_curr_hp()
        attack_log.append(f"The {self.get_ability_name()} strikes {target_name}, dealing {damage_dealt} damage!\n")
        if target.is_dead():
            attack_log.append(f"{unit_name} has slain {target_name}!\n")
            target.get_space().assign_unit(None)
        return attack_log
    
    def ability_preview(self, target: Unit):
        if target == None:
            return None, None
        ability_damage = self.get_ability_value() + self.get_damage_mod()
        damage_dealt = self.calculate_damage(target, ability_damage, self.__special_damage_type)
        damage_received = 0
        self_space = self.get_action_space()
        target_space = target.get_space()
        if (target_space.get_up() == self_space
            or target_space.get_left() == self_space
            or target_space.get_right() == self_space
            or target_space.get_down() == self_space):
            splash_damage = ceil(ability_damage/2)
            damage_received = self.calculate_damage(self, splash_damage, self.__special_damage_type)
        elif target_space == self_space:
            damage_received = self.calculate_damage(self, ability_damage, self.__special_damage_type)
        return damage_dealt, damage_received

class General(Unit):
    def __init__(self, p1 = True) -> None:
        unit_type = "General"
        hp=24
        dam_val=8
        dam_type=DamageType.SLASH
        def_val=0#2
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
        ability_min_range = 0
        ability_value = 2
        super().__init__(unit_type, hp, dam_val, dam_type, def_val, arm_type, move, move_type, 
                         sprite, name_list, title_list, ability_name, ability_range, ability_min_range, ability_value)
        self.set_ability_targets(TARGET_SELF)
        
    def special_ability(self, target: Unit, space: Space):
        self.expend_ability()
        attack_log = []
        self.get_player().get_extra_turns(self.get_ability_value())
        attack_log.append(f"{self.get_name()} spurs on their forces with an {self.get_ability_name()}! Two of their units may now take an action.\n")
        return attack_log


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

def get_aura_damage_mods(unit: Unit):
    mod = 0
    # Add damage bonus if the unit is close to their General
    if unit.adjacent_to(General, True, AURA_RANGE):
        mod += AURA_MOD
    return mod
    
def get_aura_defense_mods(unit: Unit):
    mod = 0
    # Add defense bonus if the unit is close to their Healer
    if unit.adjacent_to(Healer, True, AURA_RANGE):
        mod += AURA_MOD
    # Reduce defense bonus if the unit is close to the enemy Archmage
    if unit.adjacent_to(Archmage, False, AURA_RANGE):
        mod -= AURA_MOD
    return mod