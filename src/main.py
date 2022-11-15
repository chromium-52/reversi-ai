from agents import Agent, ManualAgent, MostDisksAgent, RandomAgent
from model import State

# Runs a game of Reversi with the given agents playing black and white
def run_game(black_agent: Agent, white_agent: Agent) -> None:
    print("*** Reversi ***\n")

    state = State()

    while not state.game_over():
        print(state)

        move = (-1, -1)

        if state.turn() == state.BLACK:
            print("Black's turn")
            move = black_agent.get_action(state)
        else:
            print("White's turn")
            move = white_agent.get_action(state)
        
        print()
        
        state = state.place_disk(move)
    
    print(state)
    
    print("Game over.")
    if state.winner() == state.BLACK:
        print("Black wins!")
    else:
        print("White wins!")

# Prompts the user for a type of AI opponent to play against
def get_opponent_type() -> Agent:
    agent = None

    while agent is None:
        choice = input("\nWhich type of opponent would you like to play against?\n")

        if choice == "manual":
            agent = ManualAgent()
        elif choice == "random":
            agent = RandomAgent()
        elif choice == "most disks":
            agent = MostDisksAgent()
        else:
            print("Valid responses are 'manual', 'random', and 'most disks'\n")
    
    return agent

# Allows the user to play a complete game of Reversi through standard in/out
if __name__ == '__main__':
    print("------------------")
    print("--- Reversi AI ---")
    print("------------------\n")

    black_agent = None
    white_agent = None

    while black_agent is None or white_agent is None:
        choice = input("Which color would you like to play?\n")

        if choice == "black":
            black_agent = ManualAgent()
            white_agent = get_opponent_type()
        elif choice == "white":
            black_agent = get_opponent_type()
            white_agent = ManualAgent()
        elif choice == "neither":
            black_agent = get_opponent_type()
            white_agent = get_opponent_type()
        else:
            print("Valid responses are 'black' and 'white'\n")
    
    print("\n")

    run_game(black_agent, white_agent)
