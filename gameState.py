from gameBoard import GameBoard
from units import *

class Player:
    def __init__(self) -> None:
        self.units = [
            
        ]

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

