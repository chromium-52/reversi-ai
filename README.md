# reversi-ai

Final project for CS4100: Artificial Intelligence. Contains code for various AI agents that use the minimax algorithm with alpha-beta pruning and a neural network to play a game of [Reversi](https://www.mastersofgames.com/rules/reversi-othello-rules.htm).

## Setup

Run `pip install pygame==2.1.2`.

## Usage

### Agents

The available agents are:

- manual: the player manually chooses each move
- random: randomly select a move from the list of possible moves
- most_disks: select a move resulting in flipping the most number of the opponent's disks
- mobility: select a move that maximizes the number of moves for the player
- positional: select a move based on a grid of weights, with moves with higher total values more likely to be selected
- stability: select a move that maximizes the number of immovable disks on the board
- radius: randomly select a move, weighted by distance from center of board (moves farther away from the center of the board are more likely to be selected)
- superior: acts similar to a mobility agent in the beginning phase of the game and switches first to a positional agent, thena a most disks agent based on the number of disks on the board
- neural: uses a convolutional neural network using TensorFlow to output the optimal move from the given game state

### Options

Required options:

- `-b _agent_ [_minimax_agent_ _minimax_depth_]` or `--black _agent_ [_minimax_agent_ _minimax_depth_]`: specifies the agent that black should use in the game
- `-w _agent_ [_minimax_agent_ _minimax_depth_]` or `--white _agent_ [_minimax_agent_ _minimax_depth_]`: specifies the agent that white should use in the game

If using a minimax agent, then two additional arguments need to be passed in in addition to `minimax` to specify which agent's evaluation function to use the minimax algorithm for as well as the maximum depth to reach in the minimax tree before applying the evaluation function to the game states.

Additional options:

- `-r _num_rounds_` or `--repeat _num_rounds_`: specifies the number of rounds of the game to run. Default is 1
- `-i` or `--interactive`: whether to run the game(s) in interactive mode (using a graphical user interface) or on the command line
- `-s` or `--slow`: whether to run the game(s) in slow mode (stops the program execution for 1 second in between moves). Ignored when the `-i` option is passed in

### Example

For example, `python src/main.py`, `python src/main.py -b most_disks -w minimax random 3`
