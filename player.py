from units import (
    Unit,
    Peasant
    )

class Player:
    def __init__(self, team: str) -> None:
        self.__units = []
        self.__effected_units = []
        self.__game_state = None
        self.__turn = False
        self.__extra_turns = 0
        self.__team = team
        
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