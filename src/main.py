from model import State

def start_game() -> None:
    print("---------------")
    print("----Reversi----")
    print("---------------\n")

    state = State()

    while not state.gameOver():
        print(state)

        if state.turn() == state.BLACK:
            print("Black's turn")
        else:
            print("White's turn")

        move = (-1, -1)

        while not state.isValidMove(move):
            row = int(input("Move row: "))
            column = int(input("Move column: "))

            move = (row, column)

            if not state.isValidMove(move):
                print("Invalid move\n")
        
        state = state.placeDisk(move)

        print()
    
    print(state)
    
    print("\nGame over.")
    if state.winner == state.BLACK:
        print("Black wins!")
    else:
        print("White wins!")

if __name__ == '__main__':
    start_game()
