import argparse
import pygame

from agents import Agent, ManualAgent, RandomAgent, MostDisksAgent
from constants import WINDOW_HEIGHT, WINDOW_WIDTH

from model import State
from time import sleep
from typing import Optional

AGENT_CHOICES_MAP = {
    'manual': ManualAgent(),
    'random': RandomAgent(),
    'most_disks': MostDisksAgent(),
}

class Main:
    
    def __init__(self, black_agent: "Agent", white_agent: "Agent", slow: bool) -> None:
        self.black_agent = black_agent
        self.white_agent = white_agent
        self.slow = slow

    def run_game(self, is_interactive: bool) -> None:
        if is_interactive:
            self.run_game_gui()
        else:
            self.run_game_command_line()

    # Runs a game of Reversi with the given agents playing black and white
    def run_game_command_line(self) -> None:
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

        self.end_game_command_line(state)
        
    def end_game_command_line(self, state: State) -> None:
        print("Game over.")
        winner = state.winner()
        if winner == state.BLACK:
            print("Black wins!")
        elif winner == state.WHITE:
            print("White wins!")
        else:
            print("The game is tied!")

    def run_game_gui(self) -> None:
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Reversi')

        clock = pygame.time.Clock()
        state = State(window=window)

        while not state.game_over():
            clock.tick(60) # 60 frames per second

            for event in pygame.event.get():
            # events = pygame.event.get()
            # if len(events) == 0:
            #     continue

            # event = events[0]

                if event.type == pygame.QUIT:
                    return
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    move = State.get_coordinate_from_position(position)
                    
                    state = state.place_disk(move)

            state.repaint()
        
        self.end_game_gui(state)
        
    def end_game_gui(self, state: State) -> None:
        if not state.game_over():
            print("Game interrupted")

        print("Game over.")
        winner = state.winner()
        if winner == state.BLACK:
            print("Black wins!")
        elif winner == state.WHITE:
            print("White wins!")
        else:
            print("The game is tied!")

        pygame.quit()

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
    black_agent, white_agent = Main.get_agents(args.black, args.white)
    main = Main(black_agent, white_agent, args.slow)

    main.run_game(args.interactive)
