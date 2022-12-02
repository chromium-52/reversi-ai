import random
from model import Coordinate, State


# An interface for Reversi AI agents
class Agent:
    # Returns the best action for this state based on the agent's evaluation function 
    def get_action(self, state: State) -> Coordinate:
        max_utility = -999999
        best_action = None

        for action in state.valid_moves():
            utility = self.evaluate(state.place_disk(action))
            if utility > max_utility:
                max_utility = utility
                best_action = action

        return best_action

    # This agent's evaluation function
    def evaluate(self, state: State) -> int:
        raise NotImplementedError("Evaluation function must be implemented by subclass")


# A non-AI agent that gets a move from the user
class ManualAgent(Agent):
    def get_action(self, state: State) -> Coordinate:
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
    def evaluate(self, state: State) -> int:
        return random.randint(-100, 100)


# An AI agent that returns the move which results in the most disks for the given player
class MostDisksAgent(Agent):
    def evaluate(self, state: State) -> int:
        return state.black_disks()


class PercentDisksAgent(Agent):
    def evaluate(self, state: State) -> int:
        percent_disks = state.black_disks() / (state.black_disks() + state.white_disks())
        return int(percent_disks * 100)
