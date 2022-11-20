from agents import Agent
from model import Coordinate, State

# A minimax agent with alpha-beta pruning
class MinimaxAgent(Agent):
    # Creates a new minimax agent with the given evaluation function agent and game tree traversal depth
    def __init__(self, agent: Agent, depth: int):
        self.agent = agent
        self.depth = depth
    
    def get_action(self, state: State) -> Coordinate:
        return self.get_action_helper(state, True, self.depth, -999999, 999999)
    
    def get_action_helper(self, state: State, maximize: bool, depth: int, alpha: int, beta: int) -> Coordinate:
        if depth == self.depth or state.game_over():
            return (None, self.evaluate(state))
        
        depth = depth if maximize else depth + 1
        
        if maximize:
            max_utility = -999999
            max_action = None
            for action in state.valid_moves():
                successor_utility = self.get_action_helper(state.place_disk(action), not maximize, depth, alpha, beta)[1]
                if successor_utility > max_utility:
                    max_utility = successor_utility
                    max_action = action
                alpha = max(alpha, max_utility)
                if alpha > beta:
                    break
            return (max_action, max_utility)
        else:
            min_utility = 999999
            for action in state.valid_moves():
                successor_utility = self.get_action_helper(state.place_disk(action), not maximize, depth, alpha, beta)[1]
                min_utility = min(min_utility, successor_utility)
                beta = min(beta, min_utility)
                if beta < alpha:
                    break
            return (None, min_utility)
    
    def evaluate(self, state: State) -> int:
        return self.agent.evaluate(state)
