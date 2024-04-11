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
from clientSender import Sender

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
                    

class GameState:
    def __init__(
            self,
            player1: Player,
            player2: Player,
            board: GameBoard,
            ui,
            map : str,
            sender: Sender
            ) -> None:
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.ui = ui
        self.__turn_count = 0
        self.__current_player = None
        self.__game_over = False
        self.__map = map
        if sender is None:
            self.online = False
        else:
            self.online = True
        self.sender = sender

        self.setup_board()

    def setup_board(self):
        try:
            
            if self.player1.get_team_colour() == "white":
                player_white = True
                opp_white = False

            else:
                player_white = False
                opp_white = True

            p2_units_r1 = [Archer(opp_white), Cavalry(opp_white), Healer(opp_white), Archmage(opp_white), 
                            General(opp_white), Sorcerer(opp_white), Cavalry(opp_white), Archer(opp_white)]
            self.setup_row(0, 0, p2_units_r1, False)        
            p2_units_r2 = [Peasant(opp_white), Peasant(opp_white), Soldier(opp_white), Soldier(opp_white), 
                            Soldier(opp_white), Soldier(opp_white), Peasant(opp_white), Peasant(opp_white)]
            self.setup_row(1, 0, p2_units_r2, False) 
            self.player2.assign_units(p2_units_r1+p2_units_r2)
            self.player2.join_game(self)

            p1_units_r1 = [Archer(player_white), Cavalry(player_white), Healer(player_white), Archmage(player_white), General(player_white), Sorcerer(player_white), Cavalry(player_white), Archer(player_white)]
            self.setup_row(7, 7, p1_units_r1, True)          
            p1_units_r2 = [Peasant(player_white), Peasant(player_white), Soldier(player_white), Soldier(player_white), Soldier(player_white), Soldier(player_white), Peasant(player_white), Peasant(player_white)]
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
        team_colour = unit.get_player().get_team_colour()
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
    
    def get_map(self, map_name: str):
        map =  MapLayout.Maps[map_name]
        for i in range((len(map)-1), -1, -1):
            map.append(map[i])
        return map
    
    def select_map(self):
        if self.__map != None:
            if self.__map in MapLayout.Maps:
                return self.__map
        map_size = BOARD_COLS * BOARD_ROWS
        valid_maps = []
        for map in MapLayout.Maps:
            if (len(MapLayout.Maps[map]) * 2) == map_size:
                valid_maps.append(map)
        num_maps = len(valid_maps)
        if num_maps == 0:
            return ""
        else:
            map_choice_num = randint(0, num_maps-1)
            map_choice = valid_maps[map_choice_num]
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
    
    def game_is_over(self):
        return self.__game_over
    
    def end_game(self):
        self.player1.end_turn()
        self.player2.end_turn()
        self.__game_over = True
        
    def check_victory_conditions(self):
        p1_units = self.player1.get_unit_list()
        p2_units = self.player2.get_unit_list()
        p1_team = "White"
        p2_team = "Black"
        messages = []
        p2_victory = self.check_unit_death(self.player1, p1_units, p1_team, messages)
        p1_victory = self.check_unit_death(self.player2, p2_units, p2_team, messages)        
        if self.check_army_surrender(p1_units, p1_team, messages):
            p2_victory = True
        if self.check_army_surrender(p2_units, p2_team, messages):
            p1_victory = True
        if p1_victory or p2_victory:
            if p1_victory and not p2_victory:
                messages.append(f"The {p1_team} army is victorious!\n")
                ### VICTORY SCREEN HERE
            elif p2_victory and not p1_victory:
                messages.append(f"The {p2_team} army is victorious!\n")
                ### VICTORY SCREEN HERE
            elif p2_victory and p1_victory:
                messages.append(f"The {p1_team} and {p2_team} armies have fought to a stalemate!\n")
                ### VICTORY SCREEN HERE
            self.ui.logItems['text'].insert_endgame_divider()
            for message in messages:
                self.ui.logItems['text'].add_text(message)
            return True
        return False
    
    def check_unit_death(self, player, units, team, messages):
        victory = False
        for unit in units:
            if unit.is_dead():
                if isinstance(unit, General):
                    messages.append(f"With the fall of their General, {unit.get_name()}, the {team} army cannot continue fighting!\n")
                    victory = True
                player.remove_unit(unit)
        return victory
    
    def check_army_surrender(self, units, team, messages):
        if len(units) == 1:
            messages.append(f"With their forces decimated, the {team} army is forced to surrender.\n")
            return True
        return False
            
    def next_turn(self):

        if self.check_victory_conditions():
            self.end_game()
        else:
            if self.__current_player == None: # At start of game, set turn to Player 1
                self.__turn_count += 1
                if self.player1.get_team_colour() == "white":
                    self.set_turn(self.player1)
                else:
                    self.set_turn(self.player2)
                self.ui.logItems['text'].insert_turn_divider()
            else:
                # If the current player has an extra turn, don't change turns
                if self.__current_player.has_extra_turn(): 
                    self.__current_player.use_extra_turn()
                elif self.__current_player == self.player1:
                    self.player1.end_turn()
                    if self.online:
                        self.sender.end_turn()
                    self.set_turn(self.player2)
                    if self.player1.get_team_colour == "black":
                        self.__turn_count += 1
                    self.player2.advance_timed_effects()
                    self.ui.logItems['text'].insert_turn_divider()
                else:
                    self.player2.end_turn()
                    self.set_turn(self.player1)
                    if self.player2.get_team_colour == "black":
                        self.__turn_count += 1
                    self.__turn_count += 1
                    self.player1.advance_timed_effects()
                    self.ui.logItems['text'].insert_turn_divider()
            self.ui.logItems['text'].update_label()
            #for panel in self.ui.statsPanel:
            #self.ui.statsPanel[panel].clear()