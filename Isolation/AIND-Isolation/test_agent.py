"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

import board_test

from collections import namedtuple

import timeit

Agent = namedtuple("Agent", ["player", "name"])

from importlib import reload


def time_left(fun=timeit.default_timer):
    return 2000 #- ( 1000* fun() ) # 

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""
    #NOTE: board is 7 x 7
    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)
        
    def setUp2(self):
        reload(game_agent)
        self.player1 = 0#"Player1"
        self.player2 = 1#"Player2"
        self.game = board_test.GameState(self.player1, self.player2)
        #self.assertEqual(score, 0.0)

    
        
    def test_alphabeta(self):
        """
        tests with 5 square board from classes
        """
        print("alphabeta with new board")
        self.setUp()#2()
        agent = game_agent.AlphaBetaPlayer()
        play = agent.get_move(self.game, time_left)
        self.game = self.game.forecast_move(play)
        print("player 1: " + str(play))
        play = agent.get_move(self.game, time_left)
        self.game = self.game.forecast_move(play)
        print("player 2: " + str(play))
        play = agent.get_move(self.game, time_left)
        #self.game = self.game.forecast_move(play)
        print("player 1: " + str(play))


if __name__ == '__main__':
    unittest.main()
