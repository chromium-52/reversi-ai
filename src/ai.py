from src.model import GameState, Action

class AI:
    def find_action(self, game_state: GameState) -> Action:
        raise NotImplementedError("Method not implemented. Should be implemented in a subclass.")
