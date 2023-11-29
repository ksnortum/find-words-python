class CustomWord:
    """Holds a word and its value, with a possible definition"""
    LETTER_VALUE = {
        'a': 1,
        'b': 3,
        'c': 3,
        'd': 2,
        'e': 1,
        'f': 4,
        'g': 2,
        'h': 4,
        'i': 1,
        'j': 8,
        'k': 5,
        'l': 1,
        'm': 3,
        'n': 1,
        'o': 1,
        'p': 3,
        'q': 10,
        'r': 1,
        's': 1,
        't': 1,
        'u': 1,
        'v': 4,
        'w': 4,
        'x': 8,
        'y': 4,
        'z': 10
    }

    def __init__(self, word: str, value_word: str, is_bingo: bool, definition: str = ""):
        self.word = word.lower()
        self.value_word = value_word.lower()
        self.value = self.calculate_value() + (50 if is_bingo else 0)
        self.definition = definition

    def calculate_value(self) -> int:
        """Calculate value as total letter values from tiles, without wildcards or bingos"""
        total = 0
        if self.value_word != "":
            for letter in self.value_word:
                total += self.LETTER_VALUE[letter]

        return total

    def get_word(self):
        return self.word

    def get_value_word(self):
        return self.value_word

    def get_value(self):
        return self.value

    def get_definition(self):
        return self.definition

    def __str__(self):
        return f'{self.word} ({self.value_word}): {self.value}'

    def __eq__(self, other):
        return isinstance(other, CustomWord) \
               and other.word == self.word \
               and other.value_word == self.value_word \
               and other.value == self.value

    def __ne__(self, other):
        return not self == other
