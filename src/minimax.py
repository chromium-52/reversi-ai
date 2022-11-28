from typing import Tuple
from agents import Agent
from model import Coordinate, State

# A minimax agent with alpha-beta pruning
class MinimaxAgent(Agent):
    # Creates a new minimax agent with the given evaluation function agent and game tree traversal depth
    def __init__(self, agent: Agent, depth: int):
        self.agent = agent
        self.depth = depth
    
    def get_action(self, state: State) -> Coordinate:
        return self.get_action_helper(state, state.turn(), True, 0, -999999, 999999)[0]
    
    def get_action_helper(self, state: State, player: int, maximize: bool, depth: int, alpha: int, beta: int) -> Tuple[Coordinate, int]:
        if depth == self.depth or state.game_over():
            return self.agent.get_action(state), self.evaluate(state, player)
        
        if maximize:
            max_utility = -999999
            max_action = None
            for action in state.valid_moves():
                successor_utility = self.get_action_helper(state.place_disk(action), player, not maximize, depth + 1, alpha, beta)[1]
                if successor_utility > max_utility:
                    max_utility = successor_utility
                    max_action = action
                alpha = max(alpha, max_utility)
                if alpha > beta:
                    break
            return max_action, max_utility
        else:
            min_utility = 999999
            min_action = None # Not really necessary to keep track of; will never be returned to the top-level call
            for action in state.valid_moves():
                successor_utility = self.get_action_helper(state.place_disk(action), player, not maximize, depth + 1, alpha, beta)[1]
                if successor_utility < min_utility:
                    min_utility = successor_utility
                    min_action = action
                beta = min(beta, min_utility)
                if beta < alpha:
                    break
            return min_action, min_utility
    
    def evaluate(self, state: State, player: int) -> int:
        return self.agent.evaluate(state, player)
