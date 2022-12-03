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
    # position weights

    # https://www.sciencedirect.com/science/article/pii/S0305054806002553
    ONE = [[100, -20, 10,  5,  5, 10, -20, 100],
           [-20, -50, -2, -2, -2, -2, -50, -20],
           [ 10,  -2, -1, -1, -1, -1,  -2,  10],
           [  5,  -2, -1, -1, -1, -1,  -2,   5],
           [  5,  -2, -1, -1, -1, -1,  -2,   5],
           [ 10,  -2, -1, -1, -1, -1,  -2,  10],
           [-20, -50, -2, -2, -2, -2, -50, -20],
           [100, -20, 10,  5,  5, 10, -20, 100]]
    
    # https://www.ai.rug.nl/~mwiering/GROUP/ARTICLES/paper-othello.pdf
    TWO = [[100, -25, 10,  5,  5, 10, -25, 100],
           [-25, -25,  2,  2,  2,  2, -25, -25],
           [ 10,   2,  5,  1,  1,  5,   2,  10],
           [  5,   2,  1,  2,  2,  1,   2,   5],
           [  5,   2,  1,  2,  2,  1,   2,   5],
           [ 10,   2,  5,  1,  1,  5,   2,  10],
           [-25, -25,  2,  2,  2,  2, -25, -25],
           [100, -25, 10,  5,  5, 10, -25, 100]]

    # https://www.ai.rug.nl/~mwiering/GROUP/ARTICLES/paper-othello.pdf    
    THREE = [[ 80, -26,  24, -1,  -5,  28, -18,  76],
             [-23, -39, -18, -9,  -6,  -8, -39,  -1],
             [ 46, -16,   4,  1,  -3,   6, -20,  52],
             [-13,  -5,   2, -1,   4,   3, -12,  -2],
             [ -5,  -6,   1, -2,  -3,   0,  -9,  -5],
             [ 48, -13,  12,  5,   0,   5, -24,  41],
             [-27, -53, -11, -1, -11, -16, -58, -15],
             [ 87, -25,  27, -1,   5,  36,  -3, 100]]

    WEIGHTS = [ONE, TWO, THREE]

    # Creates a new positional agent with a grid of weights
    def __init__(self, weight_index: int = 0):
        self.weights = self.WEIGHTS[weight_index]

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
