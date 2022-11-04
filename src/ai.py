from model import GameState, Action

class AI: # interface
    def find_action(self, game_state: GameState) -> Action:
        raise NotImplementedError("Method not implemented. Should be implemented in a subclass.")

class Minimax(AI): # abstract class
    def evaluation_function(self, game_state: GameState) -> int:
        raise NotImplementedError("Method not implemented. Should be implemented in a subclass")

class Random(Minimax):
    def evaluation_function(self, game_state: GameState) -> int:
        pass
