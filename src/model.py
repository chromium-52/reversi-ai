from __future__ import annotations
from typing import List, Tuple

# A Reversi move corresponding to placing a disk on the cell at the coordinates
Action = Tuple[int, int]

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

            self.numDisks = 4
        else:
            self.board = board

            self.numDisks = 0
            for row in board:
                for cell in row:
                    if cell != 0:
                        self.numDisks += 1

    # Returns the integer corresponding to whose turn it is
    def turn(self) -> int:
        return self.numDisks % 2 + 1
    
    # Places the disk on the board if the move is valid and returns the resulting state
    # If the move is not valid, the current state is returned
    def placeDisk(self, action: Action) -> State:
        if not self.isValidMove():
            return self

        # function body

        self.numDisks += 1

        return None
    
    # Returns false if the move requested is not valid
    def isValidMove(self, action: Action) -> bool:
        
        # function body

        return None
    
    # Returns the list of valid actions from this Reversi state
    def validMoves(self) -> List[Action]:
        if self.numDisks == self.SIZE * self.SIZE:
            return []
        
        moves = [(row, col) for row in range(self.SIZE) for col in range(self.SIZE)]

        moves = list(filter(self.isValidMove, moves))

        return moves
    
    # Returns true if the game is over
    def gameOver(self) -> bool:
        return len(self.validMoves()) == 0
    
    # Returns a string representation of the board
    def __str__(self) -> str:
        boardString = ""

        for row in self.board:
            for cell in row:
                if cell == self.EMPTY:
                    boardString += "0"
                if cell == self.BLACK:
                    boardString += "1"
                if cell == self.WHITE:
                    boardString += "2"
                boardString += " "
            boardString += "\n"

        return boardString
