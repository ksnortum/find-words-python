from model.dictionary_name import DictionaryName
from model.type_of_game import TypeOfGame


class InputDataBuilder:
    """
    Builds a complex InputData object.  Possible usage:

        input_data = InputDataBuilder("sea")\\\\
            .contains("k")\\\\
            .starts_with("o")\\\\
            .build()
    """

    def __init__(self, letters) -> None:
        """Set up all the possible data fields and their defaults"""
        self.letters_data = letters
        self.contains_data = ""
        self.starts_with_data = ""
        self.ends_with_data = ""
        self.dictionary_name_data = DictionaryName.OSPD
        self.number_of_letters_data = ""
        self.game_type_data = TypeOfGame.SCRABBLE

    def contains(self, contains: str) -> 'InputDataBuilder':
        self.contains_data = contains
        return self

    def starts_with(self, starts_with: str) -> 'InputDataBuilder':
        self.starts_with_data = starts_with
        return self

    def ends_with(self, ends_with: str) -> 'InputDataBuilder':
        self.ends_with_data = ends_with
        return self

    def dictionary_name(self, dictionary_name: DictionaryName) -> 'InputDataBuilder':
        self.dictionary_name_data = dictionary_name
        return self

    def number_of_letters(self, number_of_letters: str) -> 'InputDataBuilder':
        self.number_of_letters_data = number_of_letters
        return self

    def game_type(self, type_of_game: TypeOfGame) -> 'InputDataBuilder':
        self.game_type_data = type_of_game
        return self

    def build(self):
        return InputData(self)


class InputData:
    def __init__(self, input_data_builder: InputDataBuilder) -> None:
        self.input_data_builder = input_data_builder

    def get_builder(self) -> InputDataBuilder:
        return self.input_data_builder

    def get_letters(self) -> str:
        return self.get_builder().letters_data

    def get_contains(self) -> str:
        return self.get_builder().contains_data

    def get_starts_with(self) -> str:
        return self.get_builder().starts_with_data

    def get_ends_with(self) -> str:
        return self.get_builder().ends_with_data

    def get_dictionary_name(self) -> DictionaryName:
        return self.get_builder().dictionary_name_data

    def get_number_of_letters(self) -> str:
        return self.get_builder().number_of_letters_data

    def get_game_type(self) -> TypeOfGame:
        return self.get_builder().game_type_data

    def is_scrabble(self) -> bool:
        return self.get_builder().game_type_data == TypeOfGame.SCRABBLE

    def is_crossword(self) -> bool:
        return self.get_builder().game_type_data == TypeOfGame.CROSSWORD

    def is_wordle(self) -> bool:
        return self.get_builder().game_type_data == TypeOfGame.WORDLE


# Test and usage
if __name__ == "__main__":
    input_data = InputDataBuilder("sea")\
        .contains("k")\
        .starts_with("o")\
        .build()

    print(input_data.get_letters(), input_data.get_contains(), input_data.get_starts_with())
