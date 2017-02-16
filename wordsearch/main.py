from __future__ import generator_stop

from .board import Board
from .trie import TrieNode

def board_run(start, direction, board):
  """
  A generator that yields successive values of "board" starting from "start" and
  moving in "direction", raising a StopIteration when the edge of the board is
  reached.

  Each element of "direction" will be added to the current position on every
  iteration. For example, for start = (0,0) and direction = (1,1), this will yield
  (0,0), (1,1), (2,2), etc.

  Args:
    start: a 2-tuple of ints (x,y) for where to start in "board"
    direction: a 2-tuple of ints (x,y) of which direction to iterate in. 
               Both x and y should be one of (-1, 0, 1) and (0, 0) is invalid.
    board: an instance of wordsearch.board.Board
  """
  if not all(d in (-1, 0, 1) for d in direction):
    raise ValueError('All values in direction should be one of (-1, 0, 1), got {}'.format(direction))
  if direction == (0, 0):
    raise ValueError("Direction cannot be (0, 0)")

  cur_pt = start
  try:
    while True:
      yield board[cur_pt[0], cur_pt[1]]
      cur_pt = (cur_pt[0] + direction[0], cur_pt[1] + direction[1])
  except IndexError:
    return