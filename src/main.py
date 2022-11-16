import argparse

from agents import Agent, ManualAgent, RandomAgent, MostDisksAgent
from model import State
from typing import Optional

class Main:
    
    def __init__(self, black_agent: Agent, white_agent: Agent, interactive: bool, slow: bool) -> None:
        self.black_agent = black_agent
        self.white_agent = white_agent
        self.interactive = interactive
        self.slow = slow

    def run_game(self, black_agent: Agent, white_agent: Agent) -> None:
        print("------------------")
        print("--- Reversi AI ---")
        print("------------------\n")

        state = State()

        while not state.game_over():
            print(state)

            move = (-1, -1)

            if state.turn() == state.BLACK:
                print("Black's turn\n")
                move = black_agent.get_action(state)
            else:
                print("White's turn\n")
                move = white_agent.get_action(state)
            
            state = state.place_disk(move)
        
        print(state)
        
        print("Game over.")
        if state.winner() == state.BLACK:
            print("Black wins!")
        else:
            print("White wins!")

class Util:
    @staticmethod
    def get_agents(black_agent_type: Optional[str], white_agent_type: Optional[str]) -> Agent:
        black_agent = Util.__get_agent_from_type(black_agent_type)
        white_agent = Util.__get_agent_from_type(white_agent_type)

        return black_agent, white_agent

    @staticmethod
    def __get_agent_from_type(agent_type: Optional[str]) -> Agent:
        if agent_type == 'random':
            return RandomAgent()
        if agent_type == 'most_disks':
            return MostDisksAgent()
        
        return ManualAgent()

    @staticmethod
    def show_arg_usage() -> None:
        # TODO show usage message if invalid command line args are passed
        pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Reversi AI')
    agent_choices = ('manual', 'random', 'most_disks')
    parser.add_argument('-b', '--black', choices=agent_choices)
    parser.add_argument('-w', '--white', choices=agent_choices)
    parser.add_argument('-i', '--interactive', action='store_true')
    parser.add_argument('-s', '--slow')

    args = parser.parse_args()
    black_agent, white_agent = Util.get_agents(args.black, args.white)
    main = Main(black_agent, white_agent, args.interactive, args.slow)
    main.run_game()
