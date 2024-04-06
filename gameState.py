from gameBoard import (
    GameBoard,
    MapLayout
    )

from units import (
    Unit,
    Peasant, 
    Soldier, 
    Archer, 
    Cavalry,
    Sorcerer,
    Healer,
    Archmage,
    General
    )

from constants import (
    BOARD_COLS, 
    BOARD_ROWS
    )

from random import randint

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
    
    def get_team(self):
        return self.__team

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
                    

class GameState:
    def __init__(
            self,
            player1: Player,
            player2: Player,
            board: GameBoard,
            ui
            ) -> None:
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.ui = ui
        self.__turn_count = 0
        self.__current_player = None
        self.setup_board()

    def setup_board(self):
        try:
            p2_units_r1 = [Archer(False), Cavalry(False), Healer(False), Archmage(False), 
                           General(False), Sorcerer(False), Cavalry(False), Archer(False)]
            self.setup_row(0, 0, p2_units_r1, False)        
            p2_units_r2 = [Peasant(False), Peasant(False), Soldier(False), Soldier(False), 
                           Soldier(False), Soldier(False), Peasant(False), Peasant(False)]
            self.setup_row(1, 0, p2_units_r2, False) 
            self.player2.assign_units(p2_units_r1+p2_units_r2)
            self.player2.join_game(self)

            p1_units_r1 = [Archer(), Cavalry(), Healer(), Archmage(), General(), Sorcerer(), Cavalry(), Archer()]
            self.setup_row(7, 7, p1_units_r1, True)          
            p1_units_r2 = [Peasant(), Peasant(), Soldier(), Soldier(), Soldier(), Soldier(), Peasant(), Peasant()]
            self.setup_row(6, 7, p1_units_r2, True) 
            self.player1.assign_units(p1_units_r1+p1_units_r2)
            self.player1.join_game(self)
            game_map = self.select_map()
            self.board.setup_map(game_map)
            self.board.draw_all_spaces()

            self.board.link_to_state(self)
            self.ui.link_to_state(self)
            self.next_turn()

        except Exception as e:
            print(e)
            
    def promote_unit(self, unit) -> Unit:
        team_colour = unit.get_player().get_team()
        col = unit.get_space().get_col()
        if team_colour == "white":
            team = True
        else:
            team = False
        if col == 0 or col == 7:
            new_unit = Archer(team)
        elif col == 1 or col == 6:
            new_unit = Cavalry(team)
        elif col == 2:
            if team_colour == "white":
                new_unit = Healer(team)
            else:
                new_unit = Sorcerer(team)
        elif col == 5:
            if team_colour == "white":
                new_unit = Sorcerer(team)
            else:
                new_unit = Healer(team)
        else:
            new_unit = Soldier(team)
        return new_unit

    def setup_row(self, row, col, units: list, reverse: bool):
        inc = 1
        if reverse:
            inc = -1
        try:
            for unit in units:
                if self.setup_unit(unit, row, col):
                    col += inc
                else:
                    raise Exception(f"Error: Could not place unit in row {row}, col {col}.")
        except Exception as e:
            return e
            
    def setup_unit(self, unit: Unit, row: int, col: int) -> bool:
        if self.board.place_unit(unit, row, col):
            unit._place(self.board.get_space(row, col))
            return True
        return False
    
    def select_map(self):
        map_size = BOARD_COLS * BOARD_ROWS
        valid_maps = []
        map_choice = None
        for map in MapLayout.Maps:
            if (len(MapLayout.Maps[map]) * 2) == map_size:
                valid_maps.append(MapLayout.Maps[map])
        num_maps = len(valid_maps)
        if num_maps == 0:
            return []
        else:
            map_choice_num = randint(0, num_maps-1)
            map_choice = valid_maps[map_choice_num]
            for i in range((len(map_choice)-1), -1, -1):
                map_choice.append(map_choice[i])
        return map_choice
    
    def set_turn(self, player: Player):
        self.__current_player = player
        player.start_turn()

    def get_turn(self):
        return self.__turn_count
    
    def get_current_player(self):
        return self.__current_player
    
    def get_current_player_num(self):
        if self.__current_player == self.player1:
            return 1
        if self.__current_player == self.player2:
            return 2
        else:
            return "No Current Player"
    
    def next_turn(self):
        if self.__current_player == None: # At start of game, set turn to Player 1
            self.__turn_count += 1
            self.set_turn(self.player1)
            self.ui.logItems['text'].insert_turn_divider()
        else:
            # If the current player has an extra turn, don't change turns
            if self.__current_player.has_extra_turn(): 
                self.__current_player.use_extra_turn()
            elif self.__current_player == self.player1:
                self.player1.end_turn()
                self.set_turn(self.player2)
                self.player2.advance_timed_effects()
                self.ui.logItems['text'].insert_turn_divider()
            else:
                self.player2.end_turn()
                self.set_turn(self.player1)
                self.__turn_count += 1
                self.player1.advance_timed_effects()
                self.ui.logItems['text'].insert_turn_divider()
        self.ui.logItems['text'].update_label()
        #for panel in self.ui.statsPanel:
                #self.ui.statsPanel[panel].clear()