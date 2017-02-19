# wordsearch
Wordsearches are tedious. It's more fun to teach computers do them!

## Requirements:
- python3 (tested on 3.6)

## Usage
```
$ # Search a random wordsearch board using the default dictionary, words.txt
$ ./main.py
sow
ms
my
ma
ha
re
re
fine
<snip>

$ # Filter out all the short words
$ ./main.py -m 6
mutely

$ # Search a bigger board
$ ./main.py -m 6 -i 200 -w 200
scrawl
midway
pauper
beasts
cycles
schema

$ # Search a specific board
$ ./main.py -m 6 -s test_wordsearch.txt
banker
scientist
lawyer
firefighter
builder
<snip>
```

## Technical details
This program indexes the wordlist in a [trie](https://en.wikipedia.org/wiki/Trie),
then, for every letter in the board, walks in each direction, descending into the
trie as it does. When it hits the edge of the board or the bottom of the trie, it
prints the longest word it found.

The worst-case performance of this approach, after the trie is created, is O(n*min(sqrt(n), m),
where n is the number of letters in the word search and m is the maximum depth of the trie. Note
that the sqrt implies the assumption of a square board, though that term could be replaced with the
largest dimension of the board.
