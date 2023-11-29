import unittest

from controller.word_searcher import WordSearcher, remove_capitals, lower_case_non_escaped_letters
from model.custom_word import CustomWord
from model.input_data import InputDataBuilder
from model.type_of_game import TypeOfGame


class TestWordSearcher(unittest.TestCase):
    def test_remove_capitals(self):
        actual = remove_capitals("aB", ['a', 'b', 'c'])
        expected = ['a', 'c']
        self.assertEqual(expected, actual)

    def test_remove_capitals_no_caps(self):
        actual = remove_capitals("ab", ['a', 'b', 'c'])
        expected = ['a', 'b', 'c']
        self.assertEqual(expected, actual)

    def test_lower_case_non_escaped_letters(self):
        actual = lower_case_non_escaped_letters("aBc\\bD")
        expected = "abcd"
        self.assertEqual(expected, actual)

    def test_when_input_data_is_empty_return_empty(self):
        data = InputDataBuilder("").build()
        searcher = WordSearcher(data)
        words = searcher.get_words()
        self.assertEqual([], words)

    def test_when_input_data_is_anm_return_list_of_six_words(self):
        data = InputDataBuilder("anm").build()
        expected = [
            CustomWord("am", "am", False),
            CustomWord("an", "an", False),
            CustomWord("ma", "am", False),
            CustomWord("man", "anm", False),
            CustomWord("na", "an", False),
            CustomWord("nam", "anm", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_input_data_is_an_and_contains_is_m_return_list_of_four_words(self):
        data = InputDataBuilder("an").contains("m").build()
        expected = [
            CustomWord("am", "am", False),
            CustomWord("ma", "am", False),
            CustomWord("man", "anm", False),
            CustomWord("nam", "anm", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_input_data_is_an_and_startswith_is_m_return_list_of_two_words(self):
        data = InputDataBuilder("an").starts_with("m").build()
        expected = [
            CustomWord("ma", "am", False),
            CustomWord("man", "anm", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_input_data_is_an_and_endswith_is_m_return_list_of_two_words(self):
        data = InputDataBuilder("an").ends_with("m").build()
        expected = [
            CustomWord("am", "am", False),
            CustomWord("nam", "anm", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_input_data_is_anm_and_contains_is_M_return_list_of_four_words(self):
        data = InputDataBuilder("anm").contains("M").build()
        expected = [
            CustomWord("am", "am", False),
            CustomWord("ma", "am", False),
            CustomWord("man", "anm", False),
            CustomWord("nam", "anm", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_input_data_is_as_and_contains_is_mA_return_list_of_two_words(self):
        data = InputDataBuilder("as").contains("mA").build()
        expected = [
            CustomWord("ma", "ma", False),
            CustomWord("mas", "sma", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_input_data_is_anm_and_startswith_is_M_return_list_of_two_words(self):
        data = InputDataBuilder("anm").starts_with("M").build()
        expected = [
            CustomWord("ma", "am", False),
            CustomWord("man", "anm", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_input_data_is_anm_and_endswith_is_M_return_list_of_two_words(self):
        data = InputDataBuilder("anm").ends_with("M").build()
        expected = [
            CustomWord("am", "am", False),
            CustomWord("nam", "anm", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_input_data_is_a_and_startswith_is_m_and_endswith_is_n_return_list_of_one_word(self):
        data = InputDataBuilder("a").starts_with("m").ends_with("n").build()
        expected = [
            CustomWord("man", "amn", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_input_data_is_a_and_startswith_is_m_and_contains_is_a_return_list_of_one_word(self):
        data = InputDataBuilder("a").starts_with("m").contains("a").build()
        expected = [
            CustomWord("ma", "am", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_input_data_is_a_and_startswith_m_and_contains_n_and_endswith_a_return_list_of_one_word(self):
        data = InputDataBuilder("a").starts_with("m").ends_with("a").contains("n").build()
        expected = [
            CustomWord("mana", "anma", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_input_data_is_bdot_return_list_of_five_words(self):
        data = InputDataBuilder("b.").build()
        expected = [
            CustomWord("ba", "b", False),
            CustomWord("be", "b", False),
            CustomWord("bi", "b", False),
            CustomWord("bo", "b", False),
            CustomWord("by", "b", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_input_data_is_bdot_and_endswith_z_return_list_of_one_word(self):
        data = InputDataBuilder("b.").ends_with("z").build()
        expected = [
            CustomWord("biz", "bz", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_input_data_is_anm_and_contains_dotadot_return_list_of_three_words(self):
        data = InputDataBuilder("anm").contains(".a.").build()
        expected = [
            CustomWord("man", "anm", False),
            CustomWord("mana", "anma", False),
            CustomWord("nam", "anm", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_input_is_managed_return_list_with_bingo(self):
        data = InputDataBuilder("managed").build()
        bingo_word = CustomWord("managed", "managed", True)
        searcher = WordSearcher(data)
        actual_words = searcher.get_words()
        self.assertTrue(bingo_word in actual_words)
        actual_bingo = [word for word in actual_words if word == bingo_word]
        self.assertEqual(actual_bingo[0].get_value(), bingo_word.get_value())

    def test_crossword_return_list_of_four_words(self):
        data = InputDataBuilder("")\
            .game_type(TypeOfGame.CROSSWORD)\
            .number_of_letters("3")\
            .starts_with("m")\
            .ends_with("n")\
            .build()
        expected = [
            CustomWord("man", "", False),
            CustomWord("men", "", False),
            CustomWord("mon", "", False),
            CustomWord("mun", "", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)

    def test_when_wordle_test_1_return_list_of_four_words(self):
        data = InputDataBuilder("qwertyasdfghcpvzjm") \
            .game_type(TypeOfGame.WORDLE) \
            .contains("^..a") \
            .number_of_letters("5") \
            .build()
        expected = [
            CustomWord("biali", "bilia", False),
            CustomWord("blain", "bilna", False),
            CustomWord("blank", "bklna", False),
            CustomWord("llano", "lnola", False),
        ]
        searcher = WordSearcher(data)
        actual = searcher.get_words()
        self.assertListEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
