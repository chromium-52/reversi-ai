import math
import random
import pygame
from typing import Union

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


# Agent that 
#class 


# Agent that assigns weights to each of the squares on the board
#class 


class PercentDisksAgent(Agent):
    def evaluate(self, state: State) -> int:
        percent_disks = state.black_disks() / (state.black_disks() + state.white_disks())
        return int(percent_disks * 100)
    
    def __str__(self) -> str:
        return "Percent Disks"

class WeightedDiskByRadiusAgent(Agent):
    def evaluate(self, state: State) -> int:
        board = state.board
        score = 0
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == State.BLACK:
                    score += ((row - 3.5)**2 + (col - 3.5)**2) ** 0.5
        return score

    def __str__(self) -> str:
        return "Weighted Disks by Radius"
