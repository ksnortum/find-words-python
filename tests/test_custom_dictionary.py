import unittest

from model.custom_dictionary import CustomDictionary
from model.dictionary_element import DictionaryElement
from model.dictionary_name import DictionaryName


class TestCustomDictionary(unittest.TestCase):
    def setUp(self) -> None:
        self.test_words = [
            DictionaryElement("one", None),
            DictionaryElement("two", None),
            DictionaryElement("three", None)
        ]
        self.test_words_with_definitions = [
            DictionaryElement("one", "the number one"),
            DictionaryElement("two", "the number two"),
            DictionaryElement("three", "the number three")
        ]

    def test_dictionary(self):
        dictionary = CustomDictionary(DictionaryName.TWL)
        valid_words = dictionary.get_valid_words()
        self.assertListEqual(self.test_words, valid_words)

    def test_dictionary_with_definitions(self):
        dictionary = CustomDictionary(DictionaryName.COLLINS_DEFINE)
        valid_words = dictionary.get_valid_words()
        self.assertListEqual(self.test_words_with_definitions, valid_words)


if __name__ == '__main__':
    unittest.main()
