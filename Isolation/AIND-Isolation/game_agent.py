"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

timer_slack = 100.0


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    #opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
    #own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    own = len(game.get_legal_moves(player))
    #blanks = len(game.get_blank_spaces())
    heuristic = 2 * own - opp_moves
    return float(heuristic)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    #opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    own = len(game.get_legal_moves(player))
    #blanks = len(game.get_blank_spaces())
    heuristic = own - opp_moves
    return float(heuristic)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    #opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))
    #own_moves = len(game.get_legal_moves(player))
    #heuristic = 3 * own_moves - opponent_moves
    #return float(heuristic)
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    own = len(game.get_legal_moves(player))
    #blanks = len(game.get_blank_spaces())
    heuristic = own - 2 * opp_moves
    return float(heuristic)

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns a legal move
        # in case the search fails due to timeout
        moves = game.get_legal_moves(self)
        #initializes the best move and the depth to 0
        if not moves:
            return (-1, -1)
        best_move = moves[0]

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            move = self.minimax(game, self.search_depth)
            if move == (-1, -1):
                return best_move
            return move

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def max_value(self, state, depth):
        """
        Max value helper function as described in the AIMA text book. Returns
        the maximum score possible in the current tree level. If the maximum depth
        has been achieved it returns simply the maximum score of this level, without
        calling the min value auxiliary function.
        """

        # checks if the time is about to expire
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        # checks if we reached the desired depth
        if depth == 0:
            return self.score(state, self)

        # initializes the best result to -inf (worst possible result)
        v = float("-inf")
        
        moves = state.get_legal_moves(self)

        # iterates the legal moves and chooses the maximum score of the level below in the tree
        for move in moves:
            v = max(v, self.min_value(state.forecast_move(move), depth - 1))
        
        return v
        
    
    def min_value(self, state, depth):
        """
        Min value helper function as described in the AIMA text book. Returns
        the minimum score possible in the current tree level. If the maximum depth
        has been achieved it returns simply the minimum score of this level, without
        calling the max value auxiliary function.
        """

        # checks if the time is about to expire
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        # checks if we reached the desired depth, if so, returns the score of the agent
        if depth == 0:
            return self.score(state, self)

        # initializes the minimum score to +inf (best possible score)
        v = float("+inf")
        moves = state.get_legal_moves(state.get_opponent(self))

        # iterates the legal moves of the opponent, and chooses the one with the minimum score (the score is relative to the agent)
        # of the level below in the tree
        for move in moves:
            v = min(v, self.max_value(state.forecast_move(move), depth - 1))
        
        return v
    
    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        # checks if the time is about to expire
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        moves = game.get_legal_moves(self)
        action = (-1,-1)

        # this is the root of our tree, and its a max node, so we initialize the max score to -inf (worst possible score)
        val = float("-inf")

        # iterates the legal moves of the agent, and chooses the move with the maximum score of the level below in the tree
        for move in moves:
            temp = self.min_value(game.forecast_move(move), depth - 1)
            if temp > val:
                val = temp
                action = move
        return action


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        moves = game.get_legal_moves(self)
        #initializes the best move so it returns a legal move in case of timeout, and the depth to 1
        if not moves:
            return (-1, -1)
        best_move = moves[0]

        depth = 1
        
        # every iteration it increments the depth and runs alphabeta
        try:
            while True:
                move = self.alphabeta(game, depth)

                # if the move is valid, updates the best move, else it returns the best move so far
                if move == (-1, -1):
                    return best_move
                best_move = move
                depth += 1

        except SearchTimeout:
            pass

        return best_move


    def max_value(self, state, depth, alpha, beta):
        """
        Max value helper function as described in the AIMA text book. Returns
        the maximum score possible in the current tree level. If the maximum depth
        has been achieved it returns simply the maximum score of this level, without
        calling the min value auxiliary function.
        """
        # first, checks the timeout condition
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        
        # since it is a max node, if this is the final depth we're searching, we
        # must return the score of the agent
        if depth == 0:
            return self.score(state, self)
        
        # initializes the maximum score to -inf (minimum possible score)
        v = float("-inf")
        moves = state.get_legal_moves(self)

        # iterates the agent's legal moves, and chooses the maximum of the values of the level below in the tree
        # if the score is bigger than beta, it means the level above in the tree (min node) won't let the game reach
        # this node
        for move in moves:
            vmin = self.min_value(state.forecast_move(move), depth - 1, alpha, beta)
            # updates the maximum value
            v = max(v, vmin)
            # returns the maximum value, in case this is bigger than the maximum lower limit beta
            if v >= beta:
                return v
            # updates the value of alpha, which is the minimum upper limit
            alpha = max(alpha, v)
        return v
        
    def min_value(self, state, depth, alpha, beta):
        """
        Min value helper function as described in the AIMA text book. Returns
        the minimum score possible in the current tree level. If the maximum depth
        has been achieved it returns simply the minimum score of this level, without
        calling the max value auxiliary function.
        """
        # first, checks the timeout condition
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # this is a min node, so if it is the maximum depth we're searching, it must
        # return the score of the agent
        if depth == 0:
            return self.score(state, self)
        
        # initializes the minimum score to +inf (maximum possible score)
        v = float("+inf")
        moves = state.get_legal_moves(state.get_opponent(self))

        # iterates the legal moves of the opponent, and chooses the minimum value of the values of the level below in the tree
        # if we find a value that is inferior to alpha we return, because we know that the node in the level above is a max node,
        # and has a value of at least alpha to choose, and so the game won't reach this node
        for move in moves:
            vmax = self.max_value(state.forecast_move(move), depth - 1, alpha, beta)
            # updates the minimum value
            v = min(v, vmax)
            # returns the maximum value, in case this is bigger than the minimum upper limit beta
            if v <= alpha:
                return v
            # updates the value of beta, which is the minimum upper limit
            beta = min(beta, v)
        return v
    
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        #first checks for timeout condition
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        moves = game.get_legal_moves(self)

        action = (-1, -1)
        val = float("-inf")
        # we are currently at the first move of the player, so it will be the top
        # max node, regarding of the order that players play. Given this,
        # it iterates through all moves, and returns the one that has a maximum score
        # amoungst the child nodes. The values of alpha and beta start
        # by being -inf and +inf. In this level only alpha is updated (alpha is the best choice this node will have)
        for move in moves:
            temp = self.min_value(game.forecast_move(move), depth - 1, alpha, beta)
            if temp > val:
                val = temp
                action = move
            alpha = max(alpha, val)
        return action
