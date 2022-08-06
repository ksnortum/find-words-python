import logging
import re
from typing import Optional, List

from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot

from model.custom_dictionary import CustomDictionary
from model.custom_word import CustomWord
from model.dictionary_element import DictionaryElement
from model.input_data import InputData

ALL_LETTERS = 'abcdefghijklmnopqrstuvwxyz'


def lower_case_non_escaped_letters(string: str) -> str:
    result = []
    is_escaped_character = False
    a_thru_z = re.compile("a-zA-Z")

    for letter in string:
        if a_thru_z.fullmatch(letter) and not is_escaped_character:
            result.append(letter.lower())
        else:
            result.append(letter)

        is_escaped_character = letter == "\\"

    return ''.join(result)


def remove_capitals(letters: str) -> List[str]:
    return [letter for letter in letters if letter.islower()]


class WordSearcher(QObject):
    finished = pyqtSignal(object)
    intReady = pyqtSignal(int)

    def __init__(self, data: InputData) -> None:
        super().__init__()
        self.data = data

    @pyqtSlot()
    def get_words(self) -> Optional[List[CustomWord]]:
        logging.debug('in get_words()')
        dictionary = CustomDictionary(self.data.get_dictionary_name())
        valid_words = dictionary.get_valid_words()
        pattern = self.build_pattern()
        contains_letters = lower_case_non_escaped_letters(self.data.get_contains())
        data_letters = self.get_valid_data_letters()
        search_letters = data_letters + contains_letters + self.data.get_starts_with() + self.data.get_ends_with()
        search_letters = search_letters.lower()
        wildcards = [letter for letter in self.data.get_letters() if letter == '.']
        words = []
        increment = 100.0 / len(valid_words)
        thus_far = 0.0

        for element in valid_words:
            # logging.debug('looking at the word "%s"', element.get_word())  # TODO remove me
            self.intReady.emit(int(thus_far))
            thus_far += increment
            word = element.get_word()
            value_letters = []

            if len(word) > len(search_letters) + len(wildcards):
                continue

            if pattern is not None and not pattern.search(word):
                continue

            if (self.data.is_crossword() or self.data.is_wordle()) \
                    and self.data.get_number_of_letters().strip() != "" \
                    and len(word) != int(self.data.get_number_of_letters()):
                continue

            # TODO logging.debug('start looking at search_letters')
            word_copy = word
            for letter in search_letters:
                if letter in word_copy:
                    word_copy = word_copy.replace(letter, '', 1)
                    value_letters.append(letter)

                if len(word_copy) == 0:
                    break

            # TODO logging.debug('after looking at search_letters, word_copy is "%s"', word_copy)
            i = 0
            while len(word_copy) != 0 and i < len(wildcards):
                word_copy = word_copy(1,)
                i += 1

            if len(word_copy) == 0:
                is_bingo = len(word) - len(contains_letters) - len(self.data.get_starts_with()) \
                           - len(self.data.get_ends_with()) >= 7
                words.append(CustomWord(word, ''.join(value_letters), is_bingo, element.get_definition()))

        self.finished.emit(words)

        return words

    def build_pattern(self) -> Optional[re.Pattern]:
        pattern = None
        pattern_string = lower_case_non_escaped_letters(self.data.get_contains())

        if not self.data.get_starts_with().strip() == "":
            pattern_string = "^" + self.data.get_starts_with() + ".*" + pattern_string

        if not self.data.get_ends_with().strip() == "":
            if not pattern_string.endswith(".*"):
                pattern_string += ".*"

            pattern_string += self.data.get_ends_with().lower() + "$"

        if not pattern_string.strip() == "":
            try:
                pattern = re.compile(pattern_string)
            except re.error:
                logging.error("Built pattern '%s' but it doesn't compile", pattern_string)

        logging.debug('built pattern: %s', pattern_string)

        return pattern

    def get_valid_data_letters(self) -> str:

        # If the game is Wordle, then letters means "can't have letters"
        if self.data.is_wordle():
            data_letters = [letter for letter in ALL_LETTERS if letter not in self.data.get_letters()]
        else:
            data_letters = [letter for letter in self.data.get_letters()]

        data_letters.extend(remove_capitals(self.data.get_contains()))
        data_letters.extend(remove_capitals(self.data.get_starts_with()))
        data_letters.extend(remove_capitals(self.data.get_ends_with()))
        data_letters = [letter for letter in data_letters if letter != '.']
        result = ''.join(data_letters)

        logging.debug('valid data letters: "%s"', result)

        return result
