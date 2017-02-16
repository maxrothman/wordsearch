from wordsearch.board import Board
import unittest

class TestBoard(unittest.TestCase):
  def setUp(self):
    self.reference_board = Board([[]])
    self.reference_board._board = [
      [1,  2,  3,  4],
      [5,  6,  7,  8],
      [9, 10, 11, 12],
    ]

  def test_equals(self):
    self.assertEqual(self.reference_board, self.reference_board)

  def test_not_equals(self):
    board = Board([[]])
    board._board = [
      [1,  2,  3,  4],
      [5,  6,  7,  8],
      [9, 10, 11, 13],
    ]
    self.assertNotEqual(self.reference_board, board)

  def test_construct(self):
    board = Board([
      [1,  2,  3,  4],
      [5,  6,  7,  8],
      [9, 10, 11, 12],
    ])
    self.assertEqual(self.reference_board, board)

  def test_construct_bad_input(self):
    bad_board =[
      [1,  2,  3,  4],
      [5,  6,  7,  8],
      [9, 10, 11, 12, 13],
    ]
    self.assertRaises(ValueError, lambda: Board(bad_board))

  def test_construct_other_iterator(self):
    board = (
      (1,  2,  3,  4),
      (5,  6,  7,  8),
      (9, 10, 11, 12),
    )
    self.assertEqual(self.reference_board, Board(board))

  def test_getitem(self):
    for y, row in enumerate(self.reference_board._board):
      for x in range(len(row)):
        self.assertEqual(self.reference_board[x,y], self.reference_board._board[y][x])

  def test_getitem_wrong_type(self):
    self.assertRaises(TypeError, lambda: self.reference_board[1])

  def test_getitem_wrong_shape(self):
    self.assertRaises(ValueError, lambda: self.reference_board[1, 2, 3])

  def test_getitem_negative(self):
    self.assertRaises(IndexError, lambda: self.reference_board[-1, 0])

  def test_setitem(self):
    self.reference_board[1, 2] = 3

  def test_setitem_wrong_type(self):
    def assign():
      self.reference_board[1] = 3
    self.assertRaises(TypeError, assign)

  def test_setitem_wrong_shape(self):
    def assign():
      self.reference_board[1, 2, 3] = 3
    self.assertRaises(ValueError, assign)

  def test_setitem_negative(self):
    def assign():
      self.reference_board[-1, 0] = 3
    self.assertRaises(IndexError, assign)