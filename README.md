# find-words-python

## Find words for the games of Scrabble, Wordle, or a crossword

The app comes with a help window that explains how to use it, but in short, you enter the letters you have and press 
*Submit*.  The app will produce a list of possible words to use.  Note that it very rarely finds the one word you need. 
These are suggestions, so you're not really cheating (sort of).

This project was originally written in Perl ([scrabble-words](https://github.com/ksnortum/scrabble-words)), then 
rewritten in Java ([scrabble-words-java](https://github.com/ksnortum/scrabble-words-java)) and now rewritten in 
Python 3.  My intention is that **scrabble-words-java** and this project should stay in sync (we'll see).

I was never a Python programmer professionally -- I am self-taught, so there may be different (better) ways to do 
things.  I welcome constructive criticism.  Email me at knute (at) snortum (dot) net or submit a pull request.                                              


## Prerequisites

**find-words-python** uses the [PyQt5](https://riverbankcomputing.com/software/pyqt/intro) framework.  To install:

    pip install PyQt5

## Running

To run, cd into `<installation-directory>/find-words-python` and in Windows:

    find-word-python.bat

...or in Linux:

    ./find-words-python.sh

## Tests

**find-words-python** comes with unit testing that you can run from the command line:

    cd <installation-directory>/find-words-python/tests
    python -m unittest discover -s . -t ..


