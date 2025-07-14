class DictionaryElement:
    """One element in a dictionary list of words.  Pass in word and possible definition."""
    def __init__(self, word: str, definition: str = "") -> None:
        self.word = word
        self.definition = definition

    def get_word(self) -> str:
        return self.word

    def get_definition(self) -> str:
        return self.definition

    def __eq__(self, other):
        return isinstance(other, DictionaryElement) \
               and self.word == other.word \
               and self.definition == other.definition

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        string = self.word
        if self.definition != "":
            string += f': "{self.definition}"'

        return string
