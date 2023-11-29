import unittest

from model.dictionary_name import DictionaryName
from model.input_data import InputDataBuilder
from model.type_of_game import TypeOfGame


class TestInputData(unittest.TestCase):
    letters = "ABC"

    def test_get_letters(self):
        data = InputDataBuilder(self.letters).build()
        self.assertEqual(self.letters.lower(), data.get_letters())

    def test_get_contains(self):
        contains = "A"
        data = InputDataBuilder(self.letters).contains(contains).build()
        self.assertEqual(contains, data.get_contains())

    def test_get_dictionaries_default(self):
        data = InputDataBuilder(self.letters).build()
        self.assertEqual(DictionaryName.OSPD, data.get_dictionary_name())

    def test_get_dictionaries_set(self):
        data = InputDataBuilder(self.letters).dictionary_name(DictionaryName.TWL).build()
        self.assertEqual(DictionaryName.TWL, data.get_dictionary_name())

    def test_starts_with(self):
        starts_with = "A"
        data = InputDataBuilder(self.letters).starts_with(starts_with).build()
        self.assertEqual(starts_with, data.get_starts_with())

    def test_ends_with(self):
        ends_with = "A"
        data = InputDataBuilder(self.letters).ends_with(ends_with).build()
        self.assertEqual(ends_with, data.get_ends_with())

    def test_input_data_empty(self):
        data = InputDataBuilder("").build()
        self.assertTrue(data.is_empty())

    def test_number_of_letters(self):
        number_of_letters = "5"
        data = InputDataBuilder(self.letters).number_of_letters(number_of_letters).build()
        self.assertEqual(number_of_letters, data.get_number_of_letters())

    def test_game_type_default(self):
        data = InputDataBuilder(self.letters).build()
        self.assertEqual(TypeOfGame.SCRABBLE, data.get_game_type())

    def test_game_type(self):
        data = InputDataBuilder(self.letters).game_type(TypeOfGame.CROSSWORD).build()
        self.assertEqual(TypeOfGame.CROSSWORD, data.get_game_type())


if __name__ == '__main__':
    unittest.main()
