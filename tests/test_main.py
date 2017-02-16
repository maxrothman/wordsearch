import wordsearch.main as main
from wordsearch.board import Board
from wordsearch.trie import TrieNode
import string
from collections import Counter
import unittest

class TestBoardRun(unittest.TestCase):
  def setUp(self):
    self.board = Board([
      [1, 2, 3],
      [4, 5, 6],
      [7, 8, 9],
    ])

  def test_yields(self):
    yields = list(main.start_board_run((0,0), ( 1, 0), self.board))
    self.assertEqual(yields, [1, 2, 3])

    yields = list(main.start_board_run((0,0), ( 1, 1), self.board))
    self.assertEqual(yields, [1, 5, 9])

    yields = list(main.start_board_run((0,0), ( 0, 1), self.board))
    self.assertEqual(yields, [1, 4, 7])

    yields = list(main.start_board_run((0,0), (-1, 0), self.board))
    self.assertEqual(yields, [1])

    yields = list(main.start_board_run((0,0), (-1,-1), self.board))
    self.assertEqual(yields, [1])

    yields = list(main.start_board_run((0,0), ( 0,-1), self.board))
    self.assertEqual(yields, [1])

  def test_bad_direction(self):
    self.assertRaises(ValueError, lambda: next(main.start_board_run((0,0), (2,2), self.board)))
    self.assertRaises(ValueError, lambda: next(main.start_board_run((0,0), (0,0), self.board)))


class TestTrieSearch(unittest.TestCase):
  def setUp(self):
    self.reference_trie = TrieNode(words=['amp', 'ack', 'bus'])
    self.search = main.start_trie_search(self.reference_trie)
    next(self.search)

  def test_not_wordend(self):
    self.assertFalse(self.search.send('a'))

  def test_is_wordend(self):
    self.search.send('a')
    self.search.send('m')
    self.assertTrue(self.search.send('p'))

  def test_end_search(self):
    self.assertRaises(StopIteration, lambda: self.search.send('z'))

  def test_end_search_later(self):
    self.search.send('a')
    self.assertRaises(StopIteration, lambda: self.search.send('z'))

  def test_full_search(self):
    self.assertFalse(self.search.send('a'))
    self.assertFalse(self.search.send('m'))
    self.assertTrue(self.search.send('p'))


class TestDirections(unittest.TestCase):
  def test_has_all_directions(self):
    matrix = [
      [1, 2, 3],
      [4, 5, 6],
      [7, 8, 9],
    ]

    start = (1,1)
    # bit of a self-test
    self.assertEqual(matrix[start[1]][start[0]], 5,
      "The test itself is broken, matrix has unexpected value in starting position")

    results = {matrix[start[1] + direc[0]][start[0] + direc[1]] for direc in main.directions()}
    # Should skip 5
    self.assertEqual(results, {1, 2, 3, 4, 6, 7, 8, 9})


class TestSearchBoard(unittest.TestCase):
  def test_search(self):
    root = TrieNode(words=['amp', 'ack', 'bus', 'bar'])
    board = Board([
      ['z', 'a', 'm', 'x'],
      ['s', 'a', 'u', 'b'],
      ['u', 'm', 'c', 'a'],
      ['b', 'p', 'a', 'k'],
    ])

    self.assertEqual(set(main.search_board(board, root)), {'amp', 'ack', 'bus'})


class TestRandomBoard(unittest.TestCase):
  def test_dimensions(self):
    def verify_dimensions(width, height):
      board = main.random_board(width, height)
      self.assertEqual(board.width, width)
      self.assertEqual(board.height, height)

    verify_dimensions(1, 1)
    verify_dimensions(1, 10)
    verify_dimensions(10, 1)
    verify_dimensions(10, 10)

  def test_all_lowercase_letters(self):
    board = main.random_board(10, 10)
    for _, _, letter in board:
      self.assertIn(letter, string.ascii_lowercase)
