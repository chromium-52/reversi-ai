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

            self.blackDisks = 2
            self.whiteDisks = 2
        else:
            self.board = board

            self.blackDisks = 0
            self.whiteDisks = 0
            for row in board:
                for cell in row:
                    if cell == self.BLACK:
                        self.blackDisks += 1
                    if cell == self.WHITE:
                        self.whiteDisks += 1

    # Returns the integer corresponding to whose turn it is
    def turn(self) -> int:
        return (self.blackDisks + self.whiteDisks) % 2 + 1
    
    # Places the disk on the board if the move is valid and returns the resulting state
    # If the move is not valid, the current state is returned
    def placeDisk(self, action: Action) -> State:
        if not self.isValidMove(action):
            return self
        
        turn = self.turn()
        
        board = [[self.board[row][col] for col in range(self.SIZE)] for row in range(self.SIZE)]

        row = action[0]
        col = action[1]

        board[row][col] = turn

        directions = self.validMoveDirections(action)

        for direction in directions:
            rowDelta = direction[0]
            colDelta = direction[1]

            newRow = row + rowDelta
            newCol = col + colDelta

            while board[newRow][newCol] == turn % 2 + 1:
                board[newRow][newCol] = turn

                newRow += rowDelta
                newCol += colDelta

        return State(board)
    
    # Returns false if the move requested is not valid
    def isValidMove(self, action: Action) -> bool:
        row = action[0]
        col = action[1]

        if row < 0 or row >= self.SIZE or col < 0 or col >= self.SIZE:
            return False

        return len(self.validMoveDirections(action)) != 0
    
    # Returns the list of directions in which disks can be flipped
    def validMoveDirections(self, action: Action) -> List[Action]:
        row = action[0]
        col = action[1]

        if self.board[row][col] != 0:
            return []

        directions = [(row, col) for row in range(-1, 2) for col in range(-1, 2)]
        
        directions = list(filter(lambda direction : self.isValidMoveDirection(action, direction), directions))

        return directions

    # Returns whether disks can be flipped in a certain direction
    def isValidMoveDirection(self, action: Action, direction: Action) -> bool:
        rowDelta = direction[0]
        colDelta = direction[1]

        if rowDelta == 0 and colDelta == 0:
            return False
        
        turn = self.turn()
        
        row = action[0]
        col = action[1]

        row += rowDelta
        col += colDelta

        if row < 0 or row >= self.SIZE or col < 0 or col >= self.SIZE:
            return False
        if self.board[row][col] != turn % 2 + 1:
            return False
        
        row += rowDelta
        col += colDelta

        if row < 0 or row >= self.SIZE or col < 0 or col >= self.SIZE:
            return False

        while self.board[row][col] != turn:
            if self.board[row][col] != turn % 2 + 1:
                return False

            row += rowDelta
            col += colDelta

            if row < 0 or row >= self.SIZE or col < 0 or col >= self.SIZE:
                return False
        
        return True
    
    # Returns the list of valid actions from this Reversi state
    def validMoves(self) -> List[Action]:
        if self.blackDisks + self.whiteDisks == self.SIZE * self.SIZE:
            return []
        
        moves = [(row, col) for row in range(self.SIZE) for col in range(self.SIZE)]

        moves = list(filter(self.isValidMove, moves))

        return moves
    
    # Returns true if the game is over
    def gameOver(self) -> bool:
        return len(self.validMoves()) == 0

    # Returns the integer representation of the player who is winning
    # Returns 0 if the game is tied
    def winner(self) -> int:
        if self.blackDisks > self.whiteDisks:
            return self.BLACK
        if self.whiteDisks > self.blackDisks:
            return self.WHITE
        return self.EMPTY
    
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
