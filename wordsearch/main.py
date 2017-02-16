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


def trie_search(root):
  """
  A generator that progressively searches down a trie. When given a letter with
  "trie_search.send(letter)", it does the following:
  - If the letter is not a child of the current node, raises a StopIteration
  - If the letter is a child of the current node, select it, and yield whether it
    ends a word as a boolean

  Note that you must "prime" the generator by calling next() or .send(None) on it
  once before .send()-ing the first letter.

  Args:
    root: root TrieNode to begin the search with
  """
  cur_node = root
  letter = None
  
  while True:
    letter = yield cur_node.word_end
    if letter in cur_node.children:
      cur_node = cur_node.children[letter]
    else:
      return
