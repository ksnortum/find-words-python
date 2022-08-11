import enum


class DictionaryName(enum.Enum):
    """
    List of valid dictionaries.  Must correspond to a text file in 'resources/'.
    End name with '_DEFINE' if dictionary contains definitions of the words.
    """
    OSPD = 0
    TWL = 1
    WORDS = 2
    COLLINS = 3
    COLLINS_DEFINE = 4
