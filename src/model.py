from typing import List

class Board:
    SIZE = 8

    def __init__(self) -> None:
        self.grid = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]

    def __init__(self, grid: List[List[int]]) -> None:
        self.grid = grid

class GameState:
    def __init__(self) -> None:
        self.board = None
        self.is_player_one = True

    def __init__(self, board: Board) -> None:
        self.board = board
        self.is_player_one = True

class Coordinate:
    def __init__(self, row_index: int, col_index: int) -> None:
        self.row_index = row_index
        self.col_index = col_index

class Action:    
    def __init__(self, is_player_one: bool, location: Coordinate) -> None:
        self.is_player_one = is_player_one
        self.location = location
