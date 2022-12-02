import random
import pygame
from typing import Union

from constants import NO_MOVE, QUIT_GAME
from model import Coordinate, State

# An interface for Reversi AI agents
class Agent:
    # Returns the best action for this state based on the agent's evaluation function 
    def get_action(self, state: State) -> Coordinate:
        max_utility = -999999
        best_action = None

        for action in state.valid_moves():
            utility = self.evaluate(state.place_disk(action), state.turn())
            if utility > max_utility:
                max_utility = utility
                best_action = action
        
        return best_action
    
    # This agent's evaluation function
    def evaluate(self, state: State, player: int) -> int:
        raise NotImplementedError("Evaluation function must be implemented by subclass")

# A non-AI agent that gets a move from the user
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

# An AI agent that randomly picks a move
class RandomAgent(Agent):
    def evaluate(self, state: State, player: int) -> int:
        return random.randint(-100, 100)

# An AI agent that returns the move which results in the most disks for the given player
class MostDisksAgent(Agent):
    def evaluate(self, state: State, player: int) -> int:
        if player == State.BLACK:
            return state.black_disks()

        if player == State.WHITE:
            return state.white_disks()
