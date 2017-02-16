#!/usr/bin/env python3

from wordsearch.main import random_board, search_board
from wordsearch.trie import TrieNode
from wordsearch.board import Board
from argparse import ArgumentParser, FileType, ArgumentDefaultsHelpFormatter

description = """
Wordsearches are tedious, so it's more fun to make computers do them. This tool
searches for words in a random board.
"""

def parse_args():
  parser = ArgumentParser(description=description, formatter_class=ArgumentDefaultsHelpFormatter)

  parser.add_argument('-i', '--height', dest='height', type=int, default=100,
    help="Length of the random board")
  parser.add_argument('-w', '--width', dest='width', type=int, default=100,
    help="Width of the random board")
  parser.add_argument('-d', '--dictionary', dest='dictionary', type=FileType('r'), default='words.txt',
    help="Override for dictionary to use for wordsearch")
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
    board = Board([list(line.strip()) for line in args.wordsearch])
  else:
    board = random_board(args.width, args.height)

  rootnode = TrieNode()
  for word in args.dictionary:
    rootnode.index(word.strip())

  for word in search_board(board, rootnode):
    if len(word) >= args.min_word_length:
      print(word)


if __name__ == '__main__':
  main()