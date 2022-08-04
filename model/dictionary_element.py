class DictionaryElement:
    def __init__(self, word, definition=None):
        self.word = word
        self.definition = definition

    def get_word(self):
        return self.word

    def get_definition(self):
        return self.definition
