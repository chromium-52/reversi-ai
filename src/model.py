from __future__ import annotations
from typing import List, Tuple

# A 0-indexed row, column coordinate pair on a Reversi board
Coordinate = Tuple[int, int]

# A complete Reversi game state
class State:
    # The row and column dimension of the board for this game
    SIZE = 8

    # Integer representations for each individual board cell state
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    # Creates a new Reversi game state
    # If board is None, creates a board for a new game
    def __init__(self, board: List[List[int]] = None) -> None:
        if board is None:
            self.board = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]

            self.board[3][3] = self.WHITE
            self.board[3][4] = self.BLACK
            self.board[4][3] = self.BLACK
            self.board[4][4] = self.WHITE
        else:
            self.board = board
    
    # Returns the number of black disks on the board
    def black_disks(self) -> int:
        black_disks = 0

        for row in self.board:
            for cell in row:
                if cell == self.BLACK:
                    black_disks += 1
        
        return black_disks

    # Returns the number of white disks on the board
    def white_disks(self) -> int:
        white_disks = 0

        for row in self.board:
            for cell in row:
                if cell == self.WHITE:
                    white_disks += 1
        
        return white_disks

    # Returns the integer corresponding to whose turn it is
    def turn(self) -> int:
        return (self.black_disks() + self.white_disks()) % 2 + 1
    
    # Places the disk on the board if the move is valid and returns the resulting state
    # If the move is not valid, the current state is returned
    def place_disk(self, action: Coordinate) -> State:
        if not self.is_valid_move(action):
            return self
        
        turn = self.turn()
        
        board = [[self.board[row][col] for col in range(self.SIZE)] for row in range(self.SIZE)]

        row, column = action

        board[row][column] = turn

        directions = self.valid_move_directions(action)

        for direction in directions:
            row_delta, column_delta = direction

            new_row = row + row_delta
            new_column = column + column_delta

            while board[new_row][new_column] == turn % 2 + 1:
                board[new_row][new_column] = turn

                new_row += row_delta
                new_column += column_delta

        return State(board)
    
    # Returns false if the move requested is not valid
    def is_valid_move(self, action: Coordinate) -> bool:
        row, column = action

        if not self.is_valid_coordinate(row, column):
            return False

        return len(self.valid_move_directions(action)) != 0
    
    def is_valid_coordinate(self, row_index: int, col_index: int) -> bool:
        return 0 <= row_index < self.SIZE and 0 <= col_index < self.SIZE

    # Returns the list of directions in which disks can be flipped
    def valid_move_directions(self, action: Coordinate) -> List[Coordinate]:
        row, column = action

        if self.board[row][column] != 0:
            return []

        directions = [(row, col) for row in range(-1, 2) for col in range(-1, 2)]
        directions = [direction for direction in directions if self.is_valid_move_direction(action, direction)]

        return directions

    # Returns whether disks can be flipped in a certain direction
    def is_valid_move_direction(self, action: Coordinate, direction: Coordinate) -> bool:
        row_delta, column_delta = direction

        if row_delta == 0 and column_delta == 0:
            return False
        
        turn = self.turn()
        
        row, column = action

        row += row_delta
        column += column_delta

        if not self.is_valid_coordinate(row, column):
            return False
        if self.board[row][column] != turn % 2 + 1:
            return False
        
        row += row_delta
        column += column_delta

        if not self.is_valid_coordinate(row, column):
            return False

        while self.board[row][column] != turn:
            if self.board[row][column] != turn % 2 + 1:
                return False

            row += row_delta
            column += column_delta

            if not self.is_valid_coordinate(row, column):
                return False
        
        return True
    
    # Returns the list of valid actions from this Reversi state
    def valid_moves(self) -> List[Coordinate]:
        if self.black_disks() + self.white_disks() == self.SIZE * self.SIZE:
            return []
        
        moves = [(row, col) for row in range(self.SIZE) for col in range(self.SIZE)]
        moves = [move for move in moves if self.is_valid_move(move)]

        return moves
    
    # Returns true if the game is over
    def game_over(self) -> bool:
        return len(self.valid_moves()) == 0

    # Returns the integer representation of the player who is winning
    # Returns 0 if the game is tied
    def winner(self) -> int:
        if self.black_disks() > self.white_disks():
            return self.BLACK
        if self.white_disks() > self.black_disks():
            return self.WHITE
        return self.EMPTY
    
    # Returns a string representation of the board
    def __str__(self) -> str:
        board_string = ""

        for row in self.board:
            for cell in row:
                if cell == self.EMPTY:
                    board_string += "0"
                if cell == self.BLACK:
                    board_string += "1"
                if cell == self.WHITE:
                    board_string += "2"
                board_string += " "
            board_string += "\n"

        return board_string
