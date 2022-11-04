from __future__ import annotations
from typing import List, Tuple

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
            self.initState()
        else:
            self.initState(board)
    
    # Initializes the board to the default Reversi starting board
    def initState(self) -> None:
        self.board = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]

        self.board[3][3] = self.WHITE
        self.board[3][4] = self.BLACK
        self.board[4][3] = self.BLACK
        self.board[4][4] = self.WHITE

        self.numDisks = 4

    # Initializes the board to any board state
    def initState(self, board: List[List[int]]) -> None:
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
        if not self.validateMove():
            return self

        # function body

        self.numDisks += 1

        return None
    
    # Returns false if the move requested is not valid
    def validateMove(self, action: Action) -> bool:
        if self.gameOver():
            return False
        
        # function body

        return None
    
    # Returns true if the game is over
    def gameOver(self) -> bool:

        #function body

        return None
    
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

# An action in the state tree for the game, which contains
class Action:
    def __init__(self, position: Tuple(int, int)) -> None:
        self.position = position
