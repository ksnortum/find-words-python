import re
from typing import List

from model.input_data import InputData

TOO_FEW_LETTERS = "You must have at least one available letter"
TOO_MANY_LETTERS = "You cannot have over 20 number of letters"
LETTERS_OR_DOTS = 'Letters can only be "a" thru "z" and dots'
NO_MORE_THAN_TWO_DOTS = "Letters can have no more than two dots"
CONTAINS_TOO_LONG = "Contains cannot have more that 20 letters"
STARTSWITH_NON_LETTERS = "StartsWith must only be letters"
ENDSWITH_NON_LETTERS = "EndsWith must only be letters"
INVALID_REGEX = "The regex is invalid"
INVALID_NUMBER = "You must enter only non-negative digits in the number of letters field"
TOO_MANY_NUM_OF_LETTERS = "The Number of Letters field can't be more then 20"
NO_ANCHOR_AND_STARTSWITH = "Can't have \"^\" anchor and letters in \"Starts With\""
NO_ANCHOR_AND_ENDSWITH = "Can't have \"$\" anchor and letters in \"Ends With\""

LETTERS_DOT_RE = "[a-z.]*"
ONLY_LETTERS_RE = "[a-zA-Z]*"


class Validator:
    def __init__(self, data: InputData) -> None:
        self.data = data
        self.letters_or_dots = re.compile(LETTERS_DOT_RE)
        self.only_letters = re.compile(ONLY_LETTERS_RE)

    def validate(self) -> List[str]:
        errors = []

        if len(self.data.get_letters()) < 1:
            errors.append(TOO_FEW_LETTERS)
        elif len(self.data.get_letters()) > 20:
            errors.append(TOO_MANY_LETTERS)

        if not self.letters_or_dots.fullmatch(self.data.get_letters()):
            errors.append(LETTERS_OR_DOTS)

        if self.data.is_scrabble() and not self.no_more_than_two_dots():
            errors.append(NO_MORE_THAN_TWO_DOTS)

        if len(self.data.get_contains()) > 20:
            errors.append(CONTAINS_TOO_LONG)

        if not self.only_letters.fullmatch(self.data.get_starts_with()):
            errors.append(STARTSWITH_NON_LETTERS)

        if not self.only_letters.fullmatch(self.data.get_ends_with()):
            errors.append(ENDSWITH_NON_LETTERS)

        try:
            re.compile(self.data.get_contains())
        except re.error:
            errors.append(INVALID_REGEX)

        if (self.data.is_crossword() or self.data.is_wordle()) and self.data.get_number_of_letters().strip() != "":
            if re.compile("\\d*").fullmatch(self.data.get_number_of_letters()) is None:
                errors.append(INVALID_NUMBER)
            elif int(self.data.get_number_of_letters()) > 20:
                errors.append(TOO_MANY_NUM_OF_LETTERS)

        if self.data.get_contains().startswith("^") and self.data.get_starts_with().strip() != "":
            errors.append(INVALID_REGEX)
            errors.append(NO_ANCHOR_AND_STARTSWITH)

        if self.data.get_contains().endswith("$") and self.data.get_ends_with().strip() != "":
            errors.append(INVALID_REGEX)
            errors.append(NO_ANCHOR_AND_ENDSWITH)

        return errors

    def no_more_than_two_dots(self) -> bool:
        dots = [letter for letter in self.data.get_letters() if letter == '.']
        return len(dots) <= 2
