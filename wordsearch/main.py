# Ensure that accidentally-raised StopIterations are transformed to RuntimeErrors
# Livin' in the future!
from __future__ import generator_stop

from wordsearch.board import Board
import string, random


def start_board_run(start, direction, board):
  """
  A generator that yields successive values of "board" starting from "start" and
  moving in "direction", raising a StopIteration when the edge of the board is
  crossed.

  "direction" is added as a vector to the current position on every iteration.
  For example, for start = (0,0) and direction = (1,1), this will yield the letters
  at (0,0), (1,1), (2,2), etc.

  Args:
    start: a 2-tuple of ints (x,y) for which coordinates to start at in "board"
    direction: a 2-tuple of ints (x,y) of which direction to iterate in. 
               Both x and y should be one of (-1, 0, 1) and (0, 0) is invalid.
    board: a Board to search in

  Yields: next letter in run (type depends on board value type)
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


def start_trie_search(root):
  """
  A generator that progressively searches down a trie. When given a letter with
  "trie_search.send(letter)", it does the following:
  - If the letter is not a child of the current node, raise a StopIteration
  - If the letter is a child of the current node, select it, and yield whether it
    ends a word

  You must "prime" the generator by calling next() or .send(None) on it
  once before .send()-ing the first letter.

  Args:
    root: root TrieNode to begin the search with

  Yields: whether the letter ends a word (bool)
  """
  cur_node = root
  letter = None
  
  while True:
    letter = yield cur_node.word_end
    try:
      cur_node = cur_node.children[letter]
    except KeyError:
      return


# List of x,y vectors (tuples) for all directions a word can be found in, i.e. forwards
# or backwards in rows or columns, and on diagonals.
# E.g. (0, 1) = down, (1, 1) = diagonal down-right, (1, 0) = right, ...
_directions = [(x, y) for x in range(-1, 2) for y in range (-1, 2) if not (x == 0 and y == 0)]


def search_board(board, rootnode):
  """
  A generator that searches for words in "board" using the trie rooted by "rootnode"
  and yields the words found.

  Args:
    board: a Board to search
    rootnode: a TrieNode that roots a trie used to identify words

  Yields: a word found in board (string)
  """
  for x, y, letter in board:
    for direction in _directions:
      board_run = start_board_run((x, y), direction, board)
      trie_search = start_trie_search(rootnode)
      next(trie_search)   #Prime trie_search
      
      letters = []
      last_word_end = None

      # Try advancing both generators until one runs out. That means we've either hit
      # the edge of the board or the bottom of the trie.
      #
      # Keep track of the letters as we go and the location of the last-found
      # word_end flag in the trie. When we hit then end, grab all the letters until
      # the last-found flag.
      try:
        while True:
          letter = next(board_run)
          letters.append(letter)
          word_end = trie_search.send(letter)
          if word_end:
            last_word_end = len(letters)
      except StopIteration:
        pass

      if last_word_end is not None:
        yield ''.join(letters[:last_word_end])


def random_board(width, height):
  """
  Returns a Board of random lowercase letters
  
  Args:
    width: width of the board
    height: height of the board
  """
  return Board([[random.choice(string.ascii_lowercase) for _ in range(width)] for _ in range(height)])