import numpy as np
import os
from typing import List

import tensorflow.keras.models as models

from model import State
from agents import Agent

ThreeDimArr = List[List[List[int]]]
Board = List[List[int]]

# Agent that uses a neural network to (attempt to) compute the optimal move
class NeuralNetworkAgent(Agent):
    def __init__(self, model_name: str = '1000_normalized.h5') -> None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.model = models.load_model(f'{dir_path}/models/{model_name}')

    def evaluate(self, state: State) -> int:
        board_3d = self.__reshape_board(state)
        board_3d = np.expand_dims(board_3d, 0)
        return self.model(board_3d)[0][0]
    
    def __reshape_board(self, state: State) -> ThreeDimArr:
        board = state.board
        board_3d = np.zeros((4, State.SIZE, State.SIZE), dtype=np.int8)

        # 3rd dimension - black, white, valid move, vulnerable disk

        # black, white
        for row_index, row in enumerate(board):
            for col_index, cell in enumerate(row):
                if cell == State.BLACK:
                    board_3d[0][row_index][col_index] = 1
                elif cell == State.WHITE:
                    board_3d[1][row_index][col_index] = 1

        # valid moves
        valid_moves = state.valid_moves()
        for row_index, col_index in valid_moves:
            board_3d[2][row_index][col_index] = 1

        # vulnerable disks
        for row_index in range(State.SIZE):
            for col_index in range(State.SIZE):
                if state.is_disk_vulnerable((row_index, col_index)):
                    board_3d[3][row_index][col_index] = 1

        return board_3d

    def __str__(self) -> str:
        return "Neural Network"
