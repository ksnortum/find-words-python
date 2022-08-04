import enum


class TypeOfGame(enum.Enum):
    """Type of game that we can find words for"""
    SCRABBLE = 0,
    CROSSWORD = 1,
    WORDLE = 2,
