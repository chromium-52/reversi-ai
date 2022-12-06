import unittest
from agents import MostDisksAgent, StabilityAgent
from minimax import MinimaxAgent
from model import State

# Testing class for Reversi state
class TestReversiState(unittest.TestCase):
    def test_constructors(self):
        state = State()

        self.assertEqual(State.BLACK, state.board[3][3])

# Testing class for Reversi move agents (test may fail because it's non-deterministic)
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

        self.assertTrue(agent.get_action(state) in [(2, 4), (4, 2)])

# Testing class for Reversi minimax agent
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

# Testing class for Reversi stability agent
class TestStabilityAgent(unittest.TestCase):
    def test_evaluate(self):
        agent = StabilityAgent()

        state = State([[1, 1, 1, 1, 2, 0, 2, 2],
                       [1, 1, 1, 0, 2, 0, 2, 2],
                       [2, 2, 2, 2, 2, 0, 2, 2],
                       [0, 0, 1, 1, 1, 0, 0, 2],
                       [1, 2, 1, 1, 2, 0, 1, 2],
                       [1, 1, 1, 0, 0, 1, 0, 1],
                       [1, 1, 1, 0, 2, 0, 1, 1],
                       [1, 1, 1, 2, 1, 1, 1, 1]])

        self.assertEqual(16, agent.evaluate(state))
        