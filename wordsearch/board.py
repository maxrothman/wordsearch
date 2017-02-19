import collections

class Board:
  """
  A wrapper class for a matrix, or in this case, a wordsearch board.

  Overrides indexing so that coordinates can be accessed as Board[x,y]. Unlike normal
  nested lists, negative indexes are invalid.
  """
  def __init__(self, board):
    """
    Create a Board from an iterable of iterables.

    Each nested iterable will become a row in the returned Board such that
    board[y][x] == Board(board)[x,y] (assuming board is indexable)

    All of the nested iterables must be of the same length, or else a ValueError will
    be raised. Neither dimension of the board can be 0, so passing board = [[]] or []
    will raise a ValueError.

    Args:
      board: an iterable of iterables
    """
    _board = [[r for r in row] for row in board]

    if not (len(_board) > 0 and len(_board[0]) > 0):
      raise ValueError("Both dimensions of the board must be greater than 0")
    if not all(len(_board[0]) == len(l) for l in _board[1:]):
      raise ValueError("Every nested iterable must be the same length")

    self._board = _board


  def __eq__(self, other):
    """
    Return True if self's underlying board list is equal to other's. Overloads the
    "==" operator.
    """
    return self._board == other._board


  def _validate_key(self, key):
    """
    Helper method for validating keys for indexing into Board. Either raises an
    exception or returns None.

    Args:
      key: key to test for validity
    """
    if not isinstance(key, collections.Sequence) or len(key) != 2:
      raise ValueError('Board must be indexed with a pair of x, y coordinates, got "{}"'.format(key))
    
    # Don't need to check if k > len(board) because the list will raise an IndexError for us.
    # This just prevents board[-1,-1] from returning a value.
    if any(k < 0 for k in key):
      raise IndexError("Board index out of range")


  def __getitem__(self, key):
    """
    Allows for accessing the coordinates in the board as Board[x,y]. Overloads
    indexing.
    """
    self._validate_key(key)
    return self._board[key[1]][key[0]]


  def __setitem__(self, key, value):
    """
    Allows for setting values in the board as Board[x,y] = val. Overloads indexing.
    """
    self._validate_key(key)
    self._board[key[1]][key[0]] = value


  @property
  def width(self):
    """Returns the width of the board (int)"""
    return len(self._board[0])


  @property
  def height(self):
    """Returns the height of the board (int)"""
    return len(self._board)


  def __iter__(self):
    """
    Yields a tuple of (x, y, letter) for each letter in the board.

    Yields:
      x: x-coordinate of yielded letter
      y: y-coordinate of yielded letter
      letter: current letter in the board
    """
    for y, row in enumerate(self._board):
      for x, letter in enumerate(row):
        yield x, y, letter
    