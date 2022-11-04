from typing import List

class Board:
    SIZE = 8

    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def __init__(self) -> None:
        self.grid = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.grid[3][3] = self.WHITE
        self.grid[3][4] = self.BLACK
        self.grid[4][3] = self.BLACK
        self.grid[4][4] = self.WHITE

    def __init__(self, grid: List[List[int]]) -> None:
        self.grid = grid

class GameState:
    def __init__(self) -> None:
        self.board = Board()
        self.is_black = True

    def __init__(self, board: Board) -> None:
        self.board = board
        self.is_black = True

    def __init__(self, board: Board, is_black: bool) -> None:
        self.board = board
        self.is_black = is_black

class Coordinate:
    def __init__(self, row_index: int, col_index: int) -> None:
        self.row_index = row_index
        self.col_index = col_index

class Action:    
    def __init__(self, is_black: bool, location: Coordinate) -> None:
        self.is_black = is_black
        self.location = location

class AI:
    def find_action(self, game_state: GameState) -> Action:
        raise NotImplementedError("Method not implemented. Should be implemented in a subclass.")
