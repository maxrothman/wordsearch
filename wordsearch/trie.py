class TrieNode:
  """
  A node in a trie.

  Note that "TrieNode.children" is not intended for modification. If you want to directly add
  children to a node, use "_add_children()".

  Usage examples:
    >>> # Create a trie with words
    >>> root = TrieNode(words=['foo', 'bar', 'baz'])
    >>> 'foo' in root
    True
    >>> 'bing' in root
    False
    >>> root.index('bing')
    >>> 'bing' in root
    True
    >>> root.children
    {'b': TrieNode(letter=b, children={a, i}), 'f': TrieNode(letter=f, children={o})}
    >>>
    >>> # Create a trie and add words later
    >>> root = TrieNode()
    >>> root.index('foo')
    >>> 'foo' in root
    True

  """
  def __init__(self, letter=None, words=None, children=None, word_end=False):
    """
    Args:
      letter: the letter this node represents, a string of length 1 or None.
              None indicates that this node is the root of the Trie.
      words: an iterable of words to index. Shortcut for iteratively calling TrieNode.index()
      children: an iterable of TrieNodes to become this node's children
      word_end: whether this node is the end of a word.
    
    "words" and "children" are mutually exclusive; providing both will raise a ValueError.
    """
    self.word_end = word_end

    if letter is None:
      pass
    elif len(letter) != 1:
      raise ValueError('"letter" should have a length of 1, got "{}"'.format(letter))
    else:
      letter = letter.lower()
    self.letter = letter

    self.children = {}

    if words is not None and children is not None:
      raise ValueError('Arguments "words" and "children" are mutually exclusive')
    elif words is not None:
      for word in words:
        self.index(word)
    elif children is not None:
      self._add_children(*children)


  def index(self, *words):
    """
    Add words to the trie

    Args:
      words: strings of words to add to the trie under this node.
    """
    if self.letter is not None:
      raise ValueError('index() should only be called on the root node')

    for word in words:
      cur_node = self
      for letter in word:
        # If the node already exists, use it
        if letter in cur_node.children:
          new_node = cur_node.children[letter]
        # Otherwise, make one
        else:
          new_node = type(self)(letter)
          cur_node._add_children(new_node)
      
        cur_node = new_node
      
      # Once we reach the end of the word, flag whichever node ends it
      cur_node.word_end = True


  def _add_children(self, *nodes):
    """
    Add children to this node

    Args:
      nodes: TrieNodes to become this node's children
    """
    if any(child.letter is None for child in nodes):
      raise ValueError("Only the root node should have letter == None")
    self.children.update({child.letter: child for child in nodes})


  def contains(self, word, prefix=False):
    """
    Return True if the trie contains "word". By default only matches whole words, but
    if "prefix" is True, then also return True if the trie contains the prefix
    "word".

    Note that this intentionally skips the current node's letter since the root node
    has no letter.
    """
    cur_node = self
    for letter in word:
      if letter in cur_node.children:
        cur_node = cur_node.children[letter]
      else:
        return False

    # If the current node doesn't end a word, return False unless prefix==True
    return cur_node.word_end or prefix


  def __contains__(self, word):
    """
    Shortcut for TrieNode.contains(word, prefix=False). Overloads "in" operator. 
    """
    return self.contains(word)


  def __eq__(self, other):
    """
    Return True if "self" has the same letter and children as "other". Overloads the
    "==" operator.
    """
    return all(getattr(self, itm) == getattr(other, itm) for itm in ['letter', 'children', 'word_end'])


  def __repr__(self):
    return "{}(letter={}, children={{{}}}, word_end={})".format(
      type(self).__name__,
      self.letter,
      ', '.join(self.children.keys()),
      self.word_end,
    )
