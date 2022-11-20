from agents import MostDisksAgent
from model import State
import unittest

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
        