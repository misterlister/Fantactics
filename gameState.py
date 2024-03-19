from gameBoard import GameBoard
from units import *

class Player:
    def __init__(self) -> None:
        self.__units = []
        self.__game_state = None
        self.__turn = False
        self.__extra_turn = False
        self.__player = False
        self.__opponent = False
        self.__colour = False

    def assign_units(self, unit_list: list):
        self.__units = unit_list
        for unit in unit_list:
            unit.set_player(self)

    def join_game(self, game):
        self.__game_state = game

    def start_turn(self):
        self.__turn = True
        
    def end_turn(self):
        self.__turn = False

    def is_current_turn(self):
        return self.__turn

    def has_extra_turn(self):
        return self.__extra_turn
    
    def set_player(self):
        self.__player = True

    def set_colour(self, colour: str):
        self.__colour = colour

    def get_colour(self) -> str:
        return self.__colour
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


    def setup_board(self):
        try:
            player_blue = (self.player1.get_colour() == "blue")
            opponent_blue = (self.player2.get_colour() == "blue")

            p2_units_r1 = [Archer(opponent_blue), Cavalry(opponent_blue), Healer(opponent_blue), Archmage(opponent_blue), 
                           General(opponent_blue), Sorcerer(opponent_blue), Cavalry(opponent_blue), Archer(opponent_blue)]
            self.setup_row(0, 0, p2_units_r1, False)        
            p2_units_r2 = [Peasant(opponent_blue), Peasant(opponent_blue), Soldier(opponent_blue), Soldier(opponent_blue), 
                           Soldier(opponent_blue), Soldier(opponent_blue), Peasant(opponent_blue), Peasant(opponent_blue)]
            self.setup_row(1, 0, p2_units_r2, False) 
            self.player2.assign_units(p2_units_r1+p2_units_r2)
            self.player2.join_game(self)

            p1_units_r1 = [Archer(player_blue), Cavalry(player_blue), Healer(player_blue), Archmage(player_blue), 
                           General(player_blue), Sorcerer(player_blue), Cavalry(player_blue), Archer(player_blue)]
            self.setup_row(7, 7, p1_units_r1, True)          
            p1_units_r2 = [Peasant(player_blue), Peasant(player_blue), Soldier(player_blue), Soldier(player_blue), 
                           Soldier(player_blue), Soldier(player_blue), Peasant(), Peasant()]
            self.setup_row(6, 7, p1_units_r2, True) 
            self.player1.assign_units(p1_units_r1+p1_units_r2)
            self.player1.join_game(self)
            self.board.draw_sprites()

            self.board.link_to_state(self)
            self.ui.link_to_state(self)
            self.next_turn()

        except Exception as e:
            print(e)

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
    
    def set_turn(self, player):
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
        self.__turn_count += 1
        if self.__current_player == None: # At start of game, set turn to Player 1
            self.set_turn(self.player1)
        else:
            # If the current player has an extra turn, don't change turns
            if self.__current_player.has_extra_turn(): 
                pass
            elif self.__current_player == self.player1:
                self.player1.end_turn()
                self.set_turn(self.player2)
            else:
                self.player2.end_turn()
                self.set_turn(self.player1)
        self.ui.logItems['text'].update_label()
        for panel in self.ui.statsPanel:
                self.ui.statsPanel[panel].clear()