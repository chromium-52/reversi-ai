import argparse

from agents import Agent, ManualAgent, RandomAgent, MostDisksAgent

from model import State
from time import sleep
from typing import Optional

AGENT_CHOICES_MAP = {
    'manual': ManualAgent(),
    'random': RandomAgent(),
    'most_disks': MostDisksAgent(),
}

class Main:
    def __init__(self, black_agent: Agent, white_agent: Agent, interactive: bool, slow: bool):
        self.black_agent = black_agent
        self.white_agent = white_agent
        self.interactive = interactive
        self.slow = slow

    # Runs a game of Reversi with the given agents playing black and white
    def run_game(self) -> None:
        print("------------------")
        print("--- Reversi AI ---")
        print("------------------\n")

        state = State()

        while not state.game_over():
            print(state)

            if state.turn() == state.BLACK:
                print("Black's turn\n")
                move = black_agent.get_action(state)
            else:
                print("White's turn\n")
                move = white_agent.get_action(state)
            
            state = state.place_disk(move)

            if self.slow:
                sleep(1) # sleep for 1 second
        
        print(state)
        
        print("Game over.")
        winner = state.winner()
        if winner == state.BLACK:
            print("Black wins!")
        elif winner == state.WHITE:
            print("White wins!")
        else:
            print("The game is tied!")

class Util:
    @staticmethod
    def get_agents(black_agent_type: Optional[str], white_agent_type: Optional[str]) -> Agent:
        black_agent = AGENT_CHOICES_MAP.get(black_agent_type, ManualAgent())
        white_agent = AGENT_CHOICES_MAP.get(white_agent_type, ManualAgent())

        return black_agent, white_agent
    
    @staticmethod
    def show_arg_usage() -> None:
        # TODO show usage message if invalid command line args are passed
        pass

# Allows the user to play a complete game of Reversi through standard in/out
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Reversi AI')
    parser.add_argument('-b', '--black', choices=AGENT_CHOICES_MAP.keys())
    parser.add_argument('-w', '--white', choices=AGENT_CHOICES_MAP.keys())
    parser.add_argument('-i', '--interactive', action='store_true')
    parser.add_argument('-s', '--slow', action='store_true')

    args = parser.parse_args()
    black_agent, white_agent = Util.get_agents(args.black, args.white)
    main = Main(black_agent, white_agent, args.interactive, args.slow)
    main.run_game()
