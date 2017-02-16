import wordsearch.main as main
from wordsearch.board import Board
from wordsearch.trie import TrieNode
import unittest

class TestBoardRun(unittest.TestCase):
  def setUp(self):
    self.board = Board([
      [1, 2, 3],
      [4, 5, 6],
      [7, 8, 9],
    ])

  def test_yields(self):
    yields = list(main.board_run((0,0), ( 1, 0), self.board))
    self.assertEqual(yields, [1, 2, 3])

    yields = list(main.board_run((0,0), ( 1, 1), self.board))
    self.assertEqual(yields, [1, 5, 9])

    yields = list(main.board_run((0,0), ( 0, 1), self.board))
    self.assertEqual(yields, [1, 4, 7])

    yields = list(main.board_run((0,0), (-1, 0), self.board))
    self.assertEqual(yields, [1])

    yields = list(main.board_run((0,0), (-1,-1), self.board))
    self.assertEqual(yields, [1])

    yields = list(main.board_run((0,0), ( 0,-1), self.board))
    self.assertEqual(yields, [1])

  def test_bad_direction(self):
    self.assertRaises(ValueError, lambda: next(main.board_run((0,0), (2,2), self.board)))
    self.assertRaises(ValueError, lambda: next(main.board_run((0,0), (0,0), self.board)))


class TestTrieSearch(unittest.TestCase):
  def setUp(self):
    self.reference_trie = TrieNode(words=['amp', 'ack', 'bus'])
    self.search = main.trie_search(self.reference_trie)
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
