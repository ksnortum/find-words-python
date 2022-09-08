import logging
import re
from typing import Optional, List

from PyQt5.QtCore import pyqtSignal, QObject, pyqtSlot

from model.custom_dictionary import CustomDictionary
from model.custom_word import CustomWord
from model.input_data import InputData

ALL_LETTERS = 'abcdefghijklmnopqrstuvwxyz'


def lower_case_non_escaped_letters(string: str) -> str:
    """Return all letters, lower cased, that aren't escaped; that is, they don't have a \\\\ in front of them"""
    result = []
    is_escaped_character = False
    a_thru_z = re.compile("[a-zA-Z]")

    for letter in string:
        if not is_escaped_character:
            if a_thru_z.fullmatch(letter):
                result.append(letter.lower())
            elif letter != "\\":
                result.append(letter)

        is_escaped_character = letter == "\\"

    return ''.join(result)


def remove_capitals(word: str, data_letters: List[str]) -> List[str]:
    """Remove all capital letters in word from data_letters"""
    for letter in word:
        if letter.isupper():
            data_letters.remove(letter.lower())

    return data_letters


class WordSearcher(QObject):
    """Find all words that match the input data"""

    # Emits a signal that this process is finished, and returns a list
    finished = pyqtSignal(list)

    # Emits a signal that this process has progressed by this percentage (0 - 100)
    intReady = pyqtSignal(int)

    def __init__(self, data: InputData) -> None:
        super().__init__()
        self.data = data

    @pyqtSlot()
    def get_words(self) -> Optional[List[CustomWord]]:
        """Return a list of dictionary words (to the caller) that match the input data."""
        logging.debug('in get_words()')
        dictionary = CustomDictionary(self.data.get_dictionary_name())
        valid_words = dictionary.get_valid_words()

        # used to filter invalid dictionary words
        pattern = self.build_pattern()

        contains_letters = self.get_letters_from_contains()
        data_letters = self.get_valid_data_letters(contains_letters)
        search_letters = data_letters + contains_letters + self.data.get_starts_with() + self.data.get_ends_with()
        search_letters = search_letters.lower()
        wildcards = [letter for letter in self.data.get_letters() if letter == '.']
        words = []
        increment = 100.0 / len(valid_words)
        thus_far = 0.0

        for element in valid_words:
            self.intReady.emit(int(thus_far))
            thus_far += increment
            word = element.get_word()
            value_letters = []

            if not self.data.is_crossword() and len(word) > len(search_letters) + len(wildcards):
                continue

            if pattern is not None and not pattern.search(word):
                continue

            if (self.data.is_crossword() or self.data.is_wordle()) \
                    and self.data.get_number_of_letters().strip() != "" \
                    and len(word) != int(self.data.get_number_of_letters()):
                continue

            if self.data.is_crossword():
                words.append(CustomWord(word, '', False, element.get_definition()))
                continue

            word_copy = word
            for letter in search_letters:
                if letter in word_copy:
                    word_copy = word_copy.replace(letter, '', 1)
                    value_letters.append(letter)

                if len(word_copy) == 0:
                    break

            i = 0
            while len(word_copy) != 0 and i < len(wildcards):
                word_copy = word_copy[1:]
                i += 1

            # Can the dictionary word be made from the search letters?
            if len(word_copy) == 0:
                is_bingo = len(word) - len(contains_letters) - len(self.data.get_starts_with()) \
                           - len(self.data.get_ends_with()) >= 7
                words.append(CustomWord(word, ''.join(value_letters), is_bingo, element.get_definition()))

        # Emit an event that tells the caller that the process is finished and passes words back
        self.finished.emit(words)

        return words  # for testing only

    def build_pattern(self) -> Optional[re.Pattern]:
        """
        To seep up searching, a pattern is built from the input data.  This pattern is not
        a perfect match of the word, but a way to screen words quickly.  At a minimum,
        dictionary words must match this pattern.

        :return: An optional pattern that the dictionary words must match
        """
        pattern = None
        pattern_string = lower_case_non_escaped_letters(self.data.get_contains())

        if not self.data.get_starts_with().strip() == "":
            pattern_string = "^" + self.data.get_starts_with().lower() + ".*" + pattern_string

        if not self.data.get_ends_with().strip() == "":
            if not pattern_string.endswith(".*"):
                pattern_string += ".*"

            pattern_string += self.data.get_ends_with().lower() + "$"

        if not pattern_string.strip() == "":
            try:
                pattern = re.compile(pattern_string)
            except re.error:
                logging.error("Built pattern %s but it doesn't compile", pattern_string)

        logging.debug('built pattern: %s', pattern_string)

        return pattern

    def get_valid_data_letters(self, contains_letters) -> str:
        """
        Since there can be a lot of non-letters in the input fields this method
        strips out all characters that shouldn't be matched against a dictionary
        word.  Capitals are removed from some fields because they are a way of saying,
        "Take this  letter from available letters when you do the match, then put it
        back afterwards."  See html/help.html.

        :return: A string of letters that the dictionary word should be matched against
        """

        # If the game is Wordle, then available letters means "can't have letters"
        if self.data.is_wordle():
            data_letters = [letter for letter in ALL_LETTERS if letter not in self.data.get_letters()]
            data_letters += data_letters + data_letters  # may have double or triple letters
        else:
            data_letters = [letter for letter in self.data.get_letters()]

        data_letters = remove_capitals(contains_letters, data_letters)
        data_letters = remove_capitals(self.data.get_starts_with(), data_letters)
        data_letters = remove_capitals(self.data.get_ends_with(), data_letters)
        data_letters = [letter for letter in data_letters if letter != '.']
        result = ''.join(data_letters)

        logging.debug('valid data letters: "%s"', result)

        return result

    def get_letters_from_contains(self) -> str:
        """Return all letters in 'contains' that aren't escaped; that is, they don't have a \\\\ in front of them"""
        result = []
        is_escaped_character = False
        a_thru_z = re.compile("[a-zA-Z]")

        for letter in self.data.get_contains():
            if a_thru_z.fullmatch(letter) and not is_escaped_character:
                result.append(letter)

            is_escaped_character = letter == "\\"

        return ''.join(result)
