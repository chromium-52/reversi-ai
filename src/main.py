import argparse
import pygame
from time import sleep
from typing import Optional

from agents import Agent, ManualAgent, MostDisksAgent, RandomAgent
from minimax import MinimaxAgent
from constants import WINDOW_HEIGHT, WINDOW_WIDTH, NO_MOVE, QUIT_GAME
from model import State

AGENT_CHOICES_MAP = {
    'manual': ManualAgent(),
    'random': RandomAgent(),
    'most_disks': MostDisksAgent(),
    'minimax': MinimaxAgent(MostDisksAgent(), 2),
}

class Main:
    def __init__(self, black_agent: Agent, white_agent: Agent, num_repeat: int, slow: bool) -> None:
        State.BLACK_agent = black_agent
        State.WHITE_agent = white_agent
        self.black_agent = black_agent
        self.white_agent = white_agent
        self.num_repeat = num_repeat
        self.slow = slow

    def run_game(self, is_interactive: bool) -> None:
        num_wins_black, num_wins_white, num_ties = 0, 0, 0

        for _ in range(self.num_repeat):
            if is_interactive:
                winner = self.run_game_gui()
            else:
                winner = self.run_game_command_line()
            
            if winner == State.BLACK:
                num_wins_black += 1
            elif winner == State.WHITE:
                num_wins_white += 1
            else:
                num_ties += 1
        
        print('GAME SUMMARY')
        print(f'Number of games played: {self.num_repeat}')
        print(f'Black ({self.black_agent}): {num_wins_black} (win rate: {round(num_wins_black / self.num_repeat * 100, 3)}%)')
        print(f'White ({self.white_agent}): {num_wins_white} (win rate: {round(num_wins_white / self.num_repeat * 100, 3)}%)')
        print(f'Ties: {num_ties}')

    # Runs a game of Reversi with the specified preferences
    def run_game_command_line(self) -> int:
        print("------------------")
        print("--- Reversi AI ---")
        print("------------------\n")

        state = State()

        while not state.game_over():
            print(state)

            if state.turn() == State.BLACK:
                print("Black's turn\n")
                move = black_agent.get_action(state)
            else:
                print("White's turn\n")
                move = white_agent.get_action(state)
            
            state = state.place_disk(move)

            if self.slow:
                sleep(1) # sleep for 1 second
        
        print(state)

        return self.end_game_command_line(state)
        
    def end_game_command_line(self, state: State) -> int:
        print("Game over.")

        winner = state.winner()
        if winner == State.BLACK:
            print("Black wins!")
        elif winner == State.WHITE:
            print("White wins!")
        else:
            print("Tie!")
        
        return winner

    def run_game_gui(self) -> int:
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Reversi')

        clock = pygame.time.Clock()
        state = State(window=window)

        state.repaint()
        sleep(2)

        while not state.game_over():
            clock.tick(60)

            curr_agent = black_agent if state.turn() == state.BLACK else white_agent
            move = curr_agent.get_action(state)

            if move == NO_MOVE or move is None:
                continue
            if move == QUIT_GAME:
                return

            state = state.place_disk(move)
            state.repaint()
            sleep(1)
        
        return self.end_game_gui(state)
        
    def end_game_gui(self, state: State) -> int:
        if not state.game_over():
            print("Game interrupted")

        print("Game over.")
        winner = state.winner()
        if winner == State.BLACK:
            print("Black wins!")
        elif winner == State.WHITE:
            print("White wins!")
        else:
            print("The game is tied!")
        print(f"Score - Black: {state.black_disks()}, White: {state.white_disks()}")

        pygame.quit()

        return winner

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
    parser = argparse.ArgumentParser(prog = 'Reversi AI')
    parser.add_argument('-b', '--black', choices = AGENT_CHOICES_MAP.keys())
    parser.add_argument('-w', '--white', choices = AGENT_CHOICES_MAP.keys())
    parser.add_argument('-r', '--repeat', type=int, default=1)
    parser.add_argument('-i', '--interactive', action = 'store_true')
    parser.add_argument('-s', '--slow', action = 'store_true')

    args = parser.parse_args()
    black_agent, white_agent = Main.get_agents(args.black, args.white)
    main = Main(black_agent, white_agent, args.repeat, args.slow)

    main.run_game(args.interactive)
