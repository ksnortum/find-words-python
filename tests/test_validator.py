import unittest

from controller.validator import Validator
from model.input_data import InputDataBuilder
from model.type_of_game import TypeOfGame


class TestValidator(unittest.TestCase):
    def test_input_no_dot(self):
        data = InputDataBuilder("abc").build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(0, len(errors))

    def test_input_one_dot(self):
        data = InputDataBuilder("ab.c").build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(0, len(errors))

    def test_input_two_dot(self):
        data = InputDataBuilder("a.b.c").build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(0, len(errors))

    def test_input_more_than_two_dots_and_crossword(self):
        data = InputDataBuilder("a.b.c.").game_type(TypeOfGame.CROSSWORD).build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(0, len(errors))

    def test_input_more_than_two_dots_and_wordle(self):
        data = InputDataBuilder("a.b.c.").game_type(TypeOfGame.WORDLE).build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(0, len(errors))

    def test_input_more_than_two_dots_and_scrabble(self):
        data = InputDataBuilder("a.b.c.").game_type(TypeOfGame.SCRABBLE).build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(1, len(errors))
        self.assertEqual(errors[0], Validator.NO_MORE_THAN_TWO_DOTS)

    def test_input_too_few_letters(self):
        data = InputDataBuilder("").build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(1, len(errors))
        self.assertEqual(errors[0], Validator.TOO_FEW_LETTERS)

    def test_no_available_letters_okay_in_crossword(self):
        data = InputDataBuilder("").game_type(TypeOfGame.CROSSWORD).build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(0, len(errors))

    def test_input_too_many_letters(self):
        data = InputDataBuilder("abcdefghijklmnopqrstuvwxyz").build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(1, len(errors))
        self.assertEqual(errors[0], Validator.TOO_MANY_LETTERS)

    def test_no_limit_on_available_letters_if_crossword(self):
        data = InputDataBuilder("abcdefghijklmnopqrstuvwxyz").game_type(TypeOfGame.CROSSWORD).build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(0, len(errors))

    def test_input_not_letters_or_dots(self):
        data = InputDataBuilder("abc5e").build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(1, len(errors))
        self.assertEqual(errors[0], Validator.LETTERS_OR_DOTS)

    def test_input_contains_too_long(self):
        data = InputDataBuilder("abc").contains("abcdefghijklmnopqrstuvwxyz").build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(1, len(errors))
        self.assertEqual(errors[0], Validator.CONTAINS_TOO_LONG)

    def test_input_startswith_not_letters(self):
        data = InputDataBuilder("abc").starts_with("a5").build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(1, len(errors))
        self.assertEqual(errors[0], Validator.STARTSWITH_NON_LETTERS)

    def test_input_endswith_not_letters(self):
        data = InputDataBuilder("abc").ends_with("a5").build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(1, len(errors))
        self.assertEqual(errors[0], Validator.ENDSWITH_NON_LETTERS)

    def test_input_numberofletters_can_be_blank(self):
        data = InputDataBuilder("abc").number_of_letters(" ").game_type(TypeOfGame.CROSSWORD).build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(0, len(errors))

    def test_input_numberofletters_is_numeric(self):
        data = InputDataBuilder("abc").number_of_letters("X").game_type(TypeOfGame.CROSSWORD).build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(1, len(errors))
        self.assertEqual(errors[0], Validator.INVALID_NUMBER)

    def test_input_numberofletters_is_twenty_or_less(self):
        data = InputDataBuilder("abc").number_of_letters("21").game_type(TypeOfGame.CROSSWORD).build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(1, len(errors))
        self.assertEqual(errors[0], Validator.TOO_MANY_NUM_OF_LETTERS)

    def test_input_contains_regex_is_invalid(self):
        data = InputDataBuilder("abc").contains("ab(de").build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(1, len(errors))
        self.assertEqual(errors[0], Validator.INVALID_REGEX)

    def test_input_contains_regex_anchor_and_startswith(self):
        data = InputDataBuilder("abc").contains("^abcde").starts_with("x").build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(2, len(errors))
        self.assertEqual(errors[0], Validator.INVALID_REGEX)
        self.assertEqual(errors[1], Validator.NO_ANCHOR_AND_STARTSWITH)

    def test_input_contains_regex_anchor_and_endswith(self):
        data = InputDataBuilder("abc").contains("abcde$").ends_with("x").build()
        validator = Validator(data)
        errors = validator.validate()
        self.assertEqual(2, len(errors))
        self.assertEqual(errors[0], Validator.INVALID_REGEX)
        self.assertEqual(errors[1], Validator.NO_ANCHOR_AND_ENDSWITH)


if __name__ == '__main__':
    unittest.main()
