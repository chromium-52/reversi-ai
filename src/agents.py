import math
import random
import pygame
from typing import List, Union

from constants import NO_MOVE, QUIT_GAME
from model import Coordinate, State


# An interface for Reversi AI agents
# All implementing evaluation functions only evaluate for black
class Agent:
    # Returns the best action for this state based on the agent's evaluation function 
    def get_action(self, state: State) -> Coordinate:
        best_action = None

        if state.turn() == State.BLACK:
            max_utility = -math.inf
            for action in state.valid_moves():
                utility = self.evaluate(state.place_disk(action))
                if utility > max_utility:
                    max_utility = utility
                    best_action = action
        else:
            min_utility = math.inf
            for action in state.valid_moves():
                utility = self.evaluate(state.place_disk(action))
                if utility < min_utility:
                    min_utility = utility
                    best_action = action

        return best_action

    # This agent's evaluation function
    def evaluate(self, state: State) -> int:
        raise NotImplementedError("Evaluation function must be implemented by subclass")


# Agent that gets a move from the user
class ManualAgent(Agent):
    def get_action(self, state: State) -> Union[Coordinate, str]:
        if state.window is not None:
            events = pygame.event.get()
            if len(events) == 0:
                return NO_MOVE

            event = events[0]
            if event.type == pygame.WINDOWCLOSE:
                return QUIT_GAME
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                return State.get_coordinate_from_position(position)
            
            return NO_MOVE

        move = (-1, -1)

        while not state.is_valid_move(move):
            row = int(input("Move row: "))
            column = int(input("Move column: "))

            move = (row, column)

            if not state.is_valid_move(move):
                print("Invalid move")

            print()

        return move
    
    def __str__(self) -> str:
        return "Manual"


# Agent that randomly picks a move
class RandomAgent(Agent):
    def evaluate(self, state: State) -> int:
        return random.randint(-1000, 1000)
    
    def __str__(self) -> str:
        return "Random"


# Agent that returns the move which results in the most disks
class MostDisksAgent(Agent):
    def evaluate(self, state: State) -> int:
        return state.black_disks() - state.white_disks()
    
    def __str__(self) -> str:
        return "Most Disks"


# Agent that returns the move which maximizes the number of moves
class MobilityAgent(Agent):
    def evaluate(self, state: State) -> int:
        if state.turn() == State.BLACK:
            return len(state.valid_moves())
        if state.turn() == State.WHITE:
            return -len(state.valid_moves)
    
    def __str__(self) -> str:
        return "Mobility"


# Agent that assigns weights to each of the positions on the board
class PositionalAgent(Agent):
    # The default position weights
    DEFAULT = [[100, -20, 10,  5,  5, 10, -20, 100],
               [-20, -50, -2, -2, -2, -2, -50, -20],
               [ 10,  -2, -1, -1, -1, -1,  -2,  10],
               [  5,  -2, -1, -1, -1, -1,  -2,   5],
               [  5,  -2, -1, -1, -1, -1,  -2,   5],
               [ 10,  -2, -1, -1, -1, -1,  -2,  10],
               [-20, -50, -2, -2, -2, -2, -50, -20],
               [100, -20, 10,  5,  5, 10, -20, 100]]

    # Creates a new positional agent with a grid of weights
    def __init__(self, weights: List[List[int]] = DEFAULT):
        self.weights = weights

    def evaluate(self, state: State) -> int:
        utility = 0

        for row in range(State.SIZE):
            for col in range(State.SIZE):
                if state.board[row][col] == State.BLACK:
                    utility += self.weights[row][col]
                if state.board[row][col] == State.WHITE:
                    utility -= self.weights[row][col]
    
    def __str__(self) -> str:
        return "Positional"
