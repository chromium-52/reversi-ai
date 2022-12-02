import math
from typing import Tuple
from agents import Agent
from model import Coordinate, State

# A minimax agent with alpha-beta pruning
class MinimaxAgent(Agent):
    # Creates a new minimax agent with the given evaluation function agent and game tree traversal depth
    def __init__(self, agent: Agent, depth: int):
        self.agent = agent
        self.depth = depth
    
    def __str__(self) -> str:
        return f"Minimax - {self.agent.__str__()}"

    def get_action(self, state: State) -> Coordinate:
        return self.get_action_helper(state, state.turn() == State.BLACK, 0, -math.inf, math.inf)[0]
    
    def get_action_helper(self, state: State, maximize: bool, depth: int, alpha: int, beta: int) -> Tuple[Coordinate, int]:
        if depth == self.depth or state.game_over():
            return None, self.evaluate(state)
        
        if maximize:
            max_utility = -math.inf
            max_action = None
            for action in state.valid_moves():
                successor_utility = self.get_action_helper(state.place_disk(action), False, depth + 1, alpha, beta)[1]
                if successor_utility > max_utility:
                    max_utility = successor_utility
                    max_action = action
                alpha = max(alpha, max_utility)
                if alpha > beta:
                    break
            return max_action, max_utility
        else:
            min_utility = math.inf
            min_action = None # Not really necessary to keep track of; will never be returned to the top-level call
            for action in state.valid_moves():
                successor_utility = self.get_action_helper(state.place_disk(action), True, depth + 1, alpha, beta)[1]
                if successor_utility < min_utility:
                    min_utility = successor_utility
                    min_action = action
                beta = min(beta, min_utility)
                if beta < alpha:
                    break
            return min_action, min_utility
    
    def evaluate(self, state: State) -> int:
        return self.agent.evaluate(state)
