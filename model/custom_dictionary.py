from typing import List

from model.dictionary_element import DictionaryElement
from model.dictionary_name import DictionaryName


class CustomDictionary:
    def __init__(self, dictionary_name: DictionaryName) -> None:
        self.dictionary_name = dictionary_name
        self.words = {}

    def get_valid_words(self) -> List[DictionaryElement]:
        if self.dictionary_name in self.words.keys():
            return self.words[self.dictionary_name]

        valid_words = []
        path = 'resources/' + self.dictionary_name.name.lower() + '.txt'
        with open(path, 'r', encoding='utf-8') as f_dictionary:
            for line in f_dictionary.readlines():
                line = line.rstrip('\n')
                parts = line.split('\t')
                word = parts[0].lower()

                if len(word) > 1:
                    definition = parts[1] if len(parts) > 1 else None
                    valid_words.append(DictionaryElement(word, definition))

        self.words[self.dictionary_name] = valid_words

        return valid_words
