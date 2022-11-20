import unittest
from agents import MostDisksAgent
from minimax import MinimaxAgent
from model import State

class TestReversiState(unittest.TestCase):
    def test_constructors(self):
        state = State()

        self.assertEqual(State.BLACK, state.board[3][4])

class TestReversiAgents(unittest.TestCase):
    def test_most_disks_agent(self):
        agent = MostDisksAgent()

        state = State([[2, 1, 0, 0, 0, 0, 0, 0],
                       [0, 2, 0, 0, 0, 0, 0, 0],
                       [0, 1, 2, 1, 0, 0, 0, 0],
                       [0, 0, 1, 1, 1, 0, 0, 0],
                       [0, 0, 0, 1, 2, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]])

        self.assertEqual((2, 4), agent.get_action(state))

class TestMinimaxAgent(unittest.TestCase):
    def test_most_disks_minimax_agent(self):
        agent = MinimaxAgent(MostDisksAgent(), 2)

        state = State([[2, 1, 0, 0, 0, 0, 0, 0],
                       [0, 2, 0, 0, 0, 0, 0, 0],
                       [0, 1, 2, 1, 0, 0, 0, 0],
                       [0, 0, 1, 1, 1, 0, 0, 0],
                       [0, 0, 0, 1, 2, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0]])

        self.assertEqual((0, 2), agent.get_action(state))
        