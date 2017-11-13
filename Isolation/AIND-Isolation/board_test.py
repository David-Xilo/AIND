
from copy import deepcopy

xlim, ylim = 3, 2  # board dimensions


class GameState:


    BLANK = 0
    NOT_MOVED = None

    def __init__(self, player_1, player_2):
        self._board = [ [0] * ylim for _ in range(xlim)]
        self._board[-1][-1] = 1
        self.move_count = 0
        self._player_1 = player_1
        self._player_2 = player_2
        self._turn = 0
        self._locations = [None, None]
        
    @property#works as an attribute, didn't know this
    def active_player(self):
        """The object registered as the player holding initiative in the
        current game state.
        """
        return self._turn
    
    @property
    def inactive_player(self):
        """The object registered as the player in waiting for the current
        game state.
        """
        return self._turn ^ 1
    
    def forecast_move(self, move):
        """ Return a new board object with the specified move
        applied to the current game state.
        
        Parameters
        ----------
        move: tuple
            The target position for the active player's next move
        """
        if move not in self.get_legal_moves(self._turn):
            raise RuntimeError("Attempted forecast of illegal move")
        newBoard = deepcopy(self)
        newBoard._board[move[0]][move[1]] = 1
        newBoard._locations[self._turn] = move
        newBoard._turn ^= 1
        return newBoard
    
    def get_legal_moves(self, player):
        """ Return a list of all legal moves available to the
        active player.  Each player should get a list of all
        empty spaces on the board on their first move, and
        otherwise they should get a list of all open spaces
        in a straight line along any row, column or diagonal
        from their current position. (Players CANNOT move
        through obstacles or blocked squares.) Moves should
        be a pair of integers in (column, row) order specifying
        the zero-indexed coordinates on the board.
        """
        loc = self._locations[player]
        if not loc:
            return self._get_blank_spaces()
        moves = []
        rays = [(1, 0), (1, -1), (0, -1), (-1, -1),
                (-1, 0), (-1, 1), (0, 1), (1, 1)]
        for dx, dy in rays:
            _x, _y = loc
            while 0 <= _x + dx < xlim and 0 <= _y + dy < ylim:
                _x, _y = _x + dx, _y + dy
                if self._board[_x][_y]:
                    break
                moves.append((_x, _y))
        return moves
        
    
    def _get_blank_spaces(self):
        """ Return a list of blank spaces on the board."""
        return [(x, y) for y in range(ylim) for x in range(xlim)
                if self._board[x][y] == 0]

    def is_loser(self, player):
        """ Test whether the specified player has lost the game. """
        return player == self._turn and not self.get_legal_moves(self._turn)
    
    def get_opponent(self, player):
        return player ^ 1