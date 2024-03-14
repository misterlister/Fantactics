from gameBoard import GameBoard
from units import *

class Player:
    def __init__(self) -> None:
        self.__units = []
        self.__game = None
        self.__turn = False
        self.__extra_turn = False

    def assign_units(self, unit_list: list):
        self.__units = unit_list
        for unit in unit_list:
            unit.set_player(self)

    def join_game(self, game: GameState):
        self.__game = game

    def start_turn(self):
        self.__turn = True
        
    def end_turn(self):
        self.__turn = False

    def is_current_turn(self):
        return self.__turn

    def has_extra_turn(self):
        return self.__extra_turn

class GameState:
    def __init__(
            self,
            player1: Player,
            player2: Player,
            board: GameBoard,
            ) -> None:
        self.player1 = player1
        self.player2 = player2
        self.board = board
        self.setup_board()
        self.__turn_count = 0
        self.__current_player = None


    def setup_board(self):
        try:
            p1_units_r1 = [Archer(), Cavalry(), Healer(), Archmage(), General(), Sorcerer(), Cavalry(), Archer()]
            self.setup_row(0, 0, p1_units_r1, False)        
            p1_units_r2 = [Peasant(), Peasant(), Soldier(), Soldier(), Soldier(), Soldier(), Peasant(), Peasant()]
            self.setup_row(1, 0, p1_units_r2, False) 
            self.player1.assign_units(p1_units_r1+p1_units_r2)
            self.player1.join_game(self)

            p2_units_r1 = [Archer(), Cavalry(), Healer(), Archmage(), General(), Sorcerer(), Cavalry(), Archer()]
            self.setup_row(7, 7, p2_units_r1, True)          
            p2_units_r2 = [Peasant(), Peasant(), Soldier(), Soldier(), Soldier(), Soldier(), Peasant(), Peasant()]
            self.setup_row(6, 7, p2_units_r2, True) 
            self.player2.assign_units(p2_units_r1+p2_units_r2)
            self.player2.join_game(self)
            self.board.draw_sprites()

            self.board.link_to_state(self)
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
        self.__current_player = self.player
        player.start_turn()
    
    def next_turn(self):
        self.__turn_count += 1
        if self.__current_player == None: # At start of game, set turn to Player 1
            self.set_turn(self.player1)
        else:
            # If the current player has an extra turn, don't change turns
            if self.__current_player.has_extra_turn(): 
                return
            elif self.__current_player == self.player1:
                self.player1.end_turn()
                self.set_turn(self.player2)
            else:
                self.player2.end_turn()
                self.set_turn(self.player1)