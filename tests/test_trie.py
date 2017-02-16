from wordsearch.trie import TrieNode
import unittest

def recursive_equal(first, second):
  """
  Return True if the tree rooted by "first" is identical to the tree rooted by
  "second", i.e. all the nodes and edges are identical.
  """
  first_queue = [first]
  second_queue = [second]
  while first_queue and second_queue:
    first_item = first_queue.pop()
    second_item = second_queue.pop()
    if first_item != second_item:
      return False

    first_queue.extend(sorted(first_item.children.values(), key=lambda x: x.letter))
    second_queue.extend(sorted(second_item.children.values(), key=lambda x: x.letter))

  if len(first_queue) != len(second_queue):
    return False

  return True

class TestRecursiveEqual(unittest.TestCase):
  def test_equal(self):
    self.assertTrue(recursive_equal(
      TrieNode(words=['amp', 'ack', 'bus']), TrieNode(words=['amp', 'ack', 'bus'])
    ))

  def test_not_equal(self):
    self.assertFalse(recursive_equal(
      TrieNode(words=['amp', 'ack', 'bus']), TrieNode(words=['amm', 'ack', 'bus'])
    ))
    self.assertFalse(recursive_equal(
      TrieNode(words=['am', 'ac', 'bus']), TrieNode(words=['amm', 'ack', 'bus'])
    ))


class TestTrie(unittest.TestCase):
  def setUp(self):
    self.reference_root = TrieNode(children=[
      TrieNode('a', children=[
        TrieNode('m', children=[
          TrieNode('p', word_end=True)
        ]),
        TrieNode('c', children=[
          TrieNode('k', word_end=True)
        ])
      ]),
      TrieNode('b', children=[
        TrieNode('u', children=[
          TrieNode('s', word_end=True)
        ])
      ])
    ])

  def test_root(self):
    root = TrieNode()
    self.assertEqual(root.children, {})
    self.assertEqual(root.letter, None)

  def test_equals(self):
    self.assertEqual(TrieNode(), TrieNode())
    self.assertEqual(TrieNode('a'), TrieNode('a'))
    self.assertEqual(TrieNode(children=[TrieNode('a')]), TrieNode(children=[TrieNode('a')]))
    self.assertEqual(TrieNode('a', children=[TrieNode('b')]), TrieNode('a', children=[TrieNode('b')]))
    self.assertEqual(TrieNode('a', word_end=True), TrieNode('a', word_end=True))

  def test_not_equals(self):
    self.assertNotEqual(TrieNode(), TrieNode('a'))
    self.assertNotEqual(TrieNode(), TrieNode(children=[TrieNode('a')]))
    self.assertNotEqual(TrieNode('a'), TrieNode('b'))
    self.assertNotEqual(TrieNode(children=[TrieNode('a')]), TrieNode(children=[TrieNode('b')]))
    self.assertNotEqual(TrieNode('c', children=[TrieNode('a')]), TrieNode('d', children=[TrieNode('a')]))
    self.assertNotEqual(TrieNode('c', children=[TrieNode('a')]), TrieNode('c', children=[TrieNode('b')]))
    self.assertNotEqual(TrieNode('a'), TrieNode('a', word_end=True))

  def test_child(self):
    root = TrieNode(children=[TrieNode('a')])
    self.assertEqual(root.letter, None)
    self.assertTrue('a' in root.children)
    self.assertEqual(root.children['a'], TrieNode('a'))

  def test_none_in_children(self):
    self.assertRaises(ValueError, lambda: TrieNode(children=[TrieNode()]))
  
  def test_lowers_letter(self):
    self.assertEqual(TrieNode('A'), TrieNode('a'))

  def test_only_one_letter(self):
    self.assertRaises(ValueError, lambda: TrieNode('ab'))

  def test_init_children_or_words(self):
    self.assertRaises(ValueError, lambda: TrieNode(children=[TrieNode('a')], words=['b']))
    
    try:
      TrieNode(children=[TrieNode('a')])
    except ValueError:
      self.fail("Should not get a ValueError when building TrieNode with only children.")
    
    try:
      TrieNode(words=['foo'])
    except ValueError:
      self.fail("Should not get a ValueError when building TrieNode with only words")

    try:
      TrieNode()
    except ValueError:
      self.fail("Should not get a ValueError when building TrieNode with no children or words")

  def test_index(self):
    root = TrieNode()
    root.index('amp', 'ack', 'bus')
    
    self.assertTrue(recursive_equal(root, self.reference_root))

  def test_construct_with_words(self):
    root = TrieNode(words=['amp', 'ack', 'bus'])
    self.assertEqual(root, self.reference_root)

  def test_construct_with_words_other_iterator(self):
    root = TrieNode(words={'amp', 'ack', 'bus'})
    self.assertEqual(root, self.reference_root)

  def test_construct_empty_wordlist(self):
    self.assertEqual(TrieNode(words=[]), TrieNode())

  def test_full_does_contain(self):
    self.assertTrue(self.reference_root.contains('amp'))
    self.assertTrue(self.reference_root.contains('ack'))
    self.assertTrue(self.reference_root.contains('bus'))

  def test_partial_does_contain(self):
    self.assertFalse(self.reference_root.contains('a'))
    self.assertFalse(self.reference_root.contains('ac'))
    self.assertFalse(self.reference_root.contains('bu'))

  def test_partial_does_contain_prefix(self):
    self.assertTrue(self.reference_root.contains('a', prefix=True))
    self.assertTrue(self.reference_root.contains('ac', prefix=True))
    self.assertTrue(self.reference_root.contains('bu', prefix=True))

  def test_does_not_contain(self):
    self.assertFalse(self.reference_root.contains('car'))
    self.assertFalse(self.reference_root.contains('candy'))
    self.assertFalse(self.reference_root.contains('amd'))
    self.assertFalse(self.reference_root.contains('adc'))
    self.assertFalse(self.reference_root.contains('bur'))
    self.assertFalse(self.reference_root.contains('apple'))

  def test_dunder_contains(self):
    self.assertTrue('amp' in self.reference_root)
    self.assertFalse('a' in self.reference_root)
    self.assertFalse('car' in self.reference_root)

  def test_repr(self):
    self.assertEqual(
      repr(TrieNode('a', children=[TrieNode('b'), TrieNode('c')])),
      "TrieNode(letter=a, children={b, c}, word_end=False)"
    )

  def test_add_chilren(self):
    root = TrieNode()
    root._add_children(TrieNode('a'))
    self.assertTrue('a' in root.children)
