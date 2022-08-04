import enum


class DictionaryName(enum.Enum):
    """List of valid dictionaries.  Must correspond to a text file in resources/"""
    OSPD = 0
    TWL = 1
    WORDS = 2
    COLINS = 3
    COLINS_DEFINE = 4
