import wordsearch.main as main
from wordsearch.board import Board
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
