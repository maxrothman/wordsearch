#!/usr/bin/env python3

from wordsearch.main import random_board, search_board
from wordsearch.trie import TrieNode
from wordsearch.board import Board
from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter
import os.path, pickle

description = """
Wordsearches are tedious. It's more fun to teach computers do them!
Either search a random board or specify a file with a grid of letters to search.
"""

def parse_args():
  parser = ArgumentParser(description=description, formatter_class=ArgumentDefaultsHelpFormatter)

  parser.add_argument('-i', '--height', dest='height', type=int, default=100,
    help="Length of the random board")
  parser.add_argument('-w', '--width', dest='width', type=int, default=100,
    help="Width of the random board")
  parser.add_argument('-d', '--dictionary', dest='dictionary', type=FileType('r'), default='words.txt',
    help="File with a list of words to search for")
  parser.add_argument('-s', '--wordsearch', dest='wordsearch', type=FileType('r'), default=None,
    help=("Search for words in a file rather than a random board."
          "The file should be a grid of lowerclase letters with no spaces or commas.")
  )
  parser.add_argument('-m' '--min-length', dest='min_word_length', type=int, default=0,
    help="Skip printing words shorter than MIN_WORD_LENGTH")

  return parser.parse_args()


def main():
  args = parse_args()

  if args.wordsearch:
    # Parse the specified wordsearch file
    board = Board([list(line.strip()) for line in args.wordsearch])
  else:
    # Use a random board
    board = random_board(args.width, args.height)

  # Pickle trie for performance
  # The cache tracks the last modified time of the dictionary.
  # If there exists a pickle cache for the dictionary's name and the file has not been
  # changed since the last cache was made, load from the pickle cache instead.
  cache_name = args.dictionary.name + '.pickle'
  cache_valid = False              #In case the cache file doesn't exist
  if os.path.exists(cache_name):
    lastmtime, rootnode = pickle.load(open(cache_name, 'rb'))
    cache_valid = lastmtime >= os.path.getmtime(args.dictionary.name)

  if not cache_valid:
    rootnode = TrieNode()
    for word in args.dictionary:
      rootnode.index(word.strip())

    pickle.dump(
      (os.path.getmtime(args.dictionary.name), rootnode),
      open(cache_name, 'wb')
    )

  for word in search_board(board, rootnode):
    if len(word) >= args.min_word_length:
      print(word)


if __name__ == '__main__':
  main()