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
        best_actions = []

        if state.turn() == State.BLACK:
            max_utility = -math.inf
            for action in state.valid_moves():
                utility = self.evaluate(state.place_disk(action))
                if utility == max_utility:
                    best_actions.append(action)
                if utility > max_utility:
                    max_utility = utility
                    best_actions = [action]
        else:
            min_utility = math.inf
            for action in state.valid_moves():
                utility = self.evaluate(state.place_disk(action))
                if utility == min_utility:
                    best_actions.append(action)
                if utility < min_utility:
                    min_utility = utility
                    best_actions = [action]
        
        if len(best_actions) == 0:
            return None
        
        if len(best_actions) == 1:
            return best_actions[0]

        return self.tiebreaker(best_actions)

    # This agent's evaluation function
    def evaluate(self, state: State) -> int:
        return 0

    # Breaks ties between actions that lead to states with the same utility
    def tiebreaker(self, actions: List[Coordinate]) -> Coordinate:
        return random.choice(actions)

    def __str__(self) -> str:
        return "Random"


# Agent that values moves that result in more disks that cannot be flipped for the rest of the game
# Doesn't work, but does something similar
class StabilityAgent(Agent):
    def evaluate(self, state: State) -> int:
        stable = self.evaluate_corner(state, True, True)
        stable += self.evaluate_corner(state, True, False)
        stable += self.evaluate_corner(state, False, True)
        stable += self.evaluate_corner(state, False, False)
        return stable
    
    def evaluate_corner(self, state: State, upper: bool, left: bool) -> int:
        stable = self.evaluate_corner_color(state, upper, left, True)
        stable += self.evaluate_corner_color(state, upper, left, False)
        return stable
        
    def evaluate_corner_color(self, state: State, upper: bool, left: bool, black: bool) -> int:
        stable = 0
        row = 0 if upper else State.SIZE - 1
        col = 0 if left else State.SIZE - 1
        if (black and state.board[row][col] == State.BLACK) or (not black and state.board[row][col] == State.WHITE):
            # Corner disk is stable
            stable = stable + 1 if black else stable - 1
            # Traverse through row until you find a non-stable disk
            col = col + 1 if left else col - 1
            while (black and state.board[row][col] == State.BLACK) or (not black and state.board[row][col] == State.WHITE):
                stable = stable + 1 if black else stable - 1
                col = col + 1 if left else col - 1
            scope = col - 1 if left else col + 1
            # Traverse through subsequent rows until you find a row where the first disk is non-stable
            row = row + 1 if upper else row - 1
            col = 0 if left else State.SIZE - 1
            while (black and state.board[row][col] == State.BLACK) or (not black and state.board[row][col] == State.WHITE):
                stable = stable + 1 if black else stable - 1
                col = col + 1 if left else col - 1
                while ((black and state.board[row][col] == State.BLACK) or (not black and state.board[row][col] == State.WHITE)) and ((left and col <= scope) or (not left and col >= scope)):
                    stable = stable + 1 if black else stable - 1
                    col = col + 1 if left else col - 1
                scope = col - 1 if left else col + 1
                row = row + 1 if upper else row - 1
                col = 0 if left else State.SIZE - 1
        return stable

    def __str__(self) -> str:
        return "Stability"


# Agent that weights moves that are farther away from the center of the board as more valuable
class RadiusAgent(Agent):
    def tiebreaker(self, actions: List[Coordinate]) -> Coordinate:
        radii = []
        for action in actions:
            radii.append((action[0] - 3.5) ** 2 + (action[1] - 3.5) ** 2)
        return random.choices(actions, weights=radii)

    def __str__(self) -> str:
        return "Radius"


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
            return -len(state.valid_moves())

    def __str__(self) -> str:
        return "Mobility"


# Agent that assigns weights to each of the positions on the board
class PositionalAgent(Agent):
    # Default position weights grid
    DEFAULT = [[100, -25,  50, 10, 10,  50, -25, 100],
               [-25, -50, -10, -5, -5, -10, -50, -25],
               [ 50, -10,   5,  1,  1,   5, -10,  50],
               [ 10,  -5,   1, -1, -1,   1,  -5,  10],
               [ 10,  -5,   1, -1, -1,   1,  -5,  10],
               [ 50, -10,   5,  1,  1,   5, -10,  50],
               [-25, -50, -10, -5, -5, -10, -50, -25],
               [100, -25,  50, 10, 10,  50, -25, 100]]

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

        return utility

    def __str__(self) -> str:
        return "Positional"


# Agent that combines evaluation functions
class CompositeAgent(Agent):
    # Creates a new composite agent with the given agents
    def __init__(self, agents: List[Agent]):
        self.agents = agents
    
    def evaluate(self, state: State) -> int:
        weights = self.get_weights(state.black_disks() + state.white_disks())

        utility = 0
        for i in range(len(self.agents)):
            utility += weights[i] * self.agents[i].evaluate(state)

        return utility
    
    # How much to weigh the evaluation functions for each agent in a given round
    def get_weights(self, num_disks: int) -> List[int]:
        return [1 for _ in self.agents]
    
    def __str__(self) -> str:
        return "Composite"
        

# Agent that wins every single time
class SuperiorAgent(CompositeAgent):
    def __init__(self):
        super().__init__([MobilityAgent(), PositionalAgent(), MostDisksAgent()])
    
    def get_weights(self, num_disks: int) -> List[int]:
        return [64 - num_disks, 64 - abs(num_disks - 32), num_disks]
    
    def __str__(self) -> str:
        return "Superior"
