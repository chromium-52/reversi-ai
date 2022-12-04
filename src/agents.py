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
        best_actions = [None]

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
class StabilityAgent(Agent):
    def evaluate(self, state: State) -> int:
        stable_disks_array = [[]]
        # populate stable disks array with false values
        for i in range(len(state.board)):
            stable_disks_array.append([])
            for j in range(len(state.board[i])):
                stable_disks_array[i].append(False)
        # mark the corners as stable if they are occupied by black
        if state.board[0][0] == State.BLACK:
            stable_disks_array[0][0] = True
        if state.board[0][7] == State.BLACK:
            stable_disks_array[0][7] = True
        if state.board[7][0] == State.BLACK:
            stable_disks_array[7][0] = True
        if state.board[7][7] == State.BLACK:
            stable_disks_array[7][7] = True
        # mark any square that is black and has a stable neighbor as stable, and repeat until no more squares are marked
        stable_disks = 0
        while True:
            marked = False
            for i in range(len(state.board)):
                for j in range(len(state.board[i])):
                    if state.board[i][j] == State.BLACK:
                        if i > 0 and stable_disks_array[i - 1][j]:
                            stable_disks_array[i][j] = True
                            marked = True
                        if i < 7 and stable_disks_array[i + 1][j]:
                            stable_disks_array[i][j] = True
                            marked = True
                        if j > 0 and stable_disks_array[i][j - 1]:
                            stable_disks_array[i][j] = True
                            marked = True
                        if j < 7 and stable_disks_array[i][j + 1]:
                            stable_disks_array[i][j] = True
                            marked = True
            if not marked:
                break
        # count the number of stable disks
        for i in range(len(state.board)):
            for j in range(len(state.board[i])):
                if stable_disks_array[i][j]:
                    stable_disks += 1
        return stable_disks

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
