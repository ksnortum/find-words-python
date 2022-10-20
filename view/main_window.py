import logging
from typing import List

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QFont, QKeySequence, QIcon
from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QLabel,
    QWidget,
    QHBoxLayout,
    QButtonGroup,
    QRadioButton,
    QGridLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QProgressBar,
    QMessageBox,
    QAction,
)
from operator import attrgetter

from controller.word_searcher import WordSearcher
from controller.validator import Validator
from model.custom_word import CustomWord
from model.dictionary_name import DictionaryName
from model.input_data import InputDataBuilder
from model.type_of_game import TypeOfGame
from view.about_page import AboutPage
from view.found_words import FoundWords
from view.help_page import HelpPage

AVAILABLE_LETTERS_TEXT = "Available Letters:"
AVAILABLE_LETTERS_TOOLTIP = "Enter the tile letters you have available, or a dot for a blank tile"
CANT_HAVE_LETTERS_TEXT = "Can't Have Letters:"
CANT_HAVE_LETTERS_TOOLTIP = "Enter the letters that these words can't have in them"
CONTAINS_LETTERS_TOOLTIP = "Letter(s)/regex on the board that words must contain"
STARTS_WITH_TOOLTIP = "Words must start with these letter(s)"
ENDS_WITH_TOOLTIP = "Words must end with these letter(s)"
NUMBER_OF_LETTERS_TOOLTIP = "The exact number of letters in a word.  Zero or blank means unlimited"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.word_searcher = None
        self.thread = None
        self.available_letters_label = None
        self.available_letters = None
        self.contains_letters = None
        self.starts_with = None
        self.ends_with = None
        self.number_of_letters = None
        self.dictionary = None
        self.submit_button = None
        self.clear_all_button = None
        self.exit_button = None
        self.progress_bar = None
        self.radio_group = None
        self.number_of_letters_clear_button = None
        self.available_letters_clear_button = None
        self.build_gui()

    def build_gui(self):
        logging.debug("building GUI")
        self.setWindowTitle("Find Words")
        self.setWindowIcon(QIcon("images/letter-S.png"))
        self.setContentsMargins(15, 0, 15, 15)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.build_menu()
        main_layout.addWidget(self.build_title())
        main_layout.addLayout(self.build_radio_buttons())
        main_layout.addLayout(self.build_grid())
        main_layout.addLayout(self.build_buttons())
        self.available_letters.setFocus()

    def build_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        clear_action = QAction("&Clear", self)
        clear_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_L))
        clear_action.triggered.connect(self.clear_all)
        file_menu.addAction(clear_action)
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q))
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        help_menu = menu.addMenu("&Help")
        help_action = QAction("&Help", self)
        help_action.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_H))
        help_action.triggered.connect(lambda: HelpPage())
        help_menu.addAction(help_action)
        about_action = QAction("&About", self)
        about_action.triggered.connect(lambda: AboutPage())
        help_menu.addAction(about_action)

    @staticmethod
    def build_title():
        title = QLabel("Find Words")
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        title.setFont(font)

        return title

    def build_radio_buttons(self):
        self.radio_group = QButtonGroup(self)
        scrabble_button = QRadioButton("Scrabble")
        scrabble_button.setChecked(True)
        self.radio_group.addButton(scrabble_button)
        crossword_button = QRadioButton("Crossword")
        self.radio_group.addButton(crossword_button)
        wordle_button = QRadioButton("Wordle")
        self.radio_group.addButton(wordle_button)
        self.radio_group.buttonClicked.connect(self.radio_button_changed)

        radio_button_box = QHBoxLayout()
        radio_button_box.addWidget(scrabble_button)
        radio_button_box.addWidget(crossword_button)
        radio_button_box.addWidget(wordle_button)

        return radio_button_box

    def build_grid(self):
        grid = QGridLayout()

        self.available_letters_label = QLabel(AVAILABLE_LETTERS_TEXT)
        row, col = 0, 0
        grid.addWidget(self.available_letters_label, row, col)
        self.available_letters = QLineEdit()
        self.available_letters.setToolTip(AVAILABLE_LETTERS_TOOLTIP)
        col = 1
        grid.addWidget(self.available_letters, row, col)
        self.available_letters_clear_button = QPushButton("Clear")
        self.available_letters_clear_button.clicked.connect(lambda: self.available_letters_clear())
        col = 2
        grid.addWidget(self.available_letters_clear_button, row, col)

        row += 1
        col = 0
        grid.addWidget(QLabel("Contains Letters:"), row, col)
        self.contains_letters = QLineEdit()
        self.contains_letters.setToolTip(CONTAINS_LETTERS_TOOLTIP)
        col = 1
        grid.addWidget(self.contains_letters, row, col)
        contains_letters_clear_button = QPushButton("Clear")
        contains_letters_clear_button.clicked.connect(lambda: self.contains_letters_clear())
        col = 2
        grid.addWidget(contains_letters_clear_button, row, col)

        row += 1
        col = 0
        grid.addWidget(QLabel("Starts with:"), row, col)
        self.starts_with = QLineEdit()
        self.starts_with.setToolTip(STARTS_WITH_TOOLTIP)
        col = 1
        grid.addWidget(self.starts_with, row, col)
        starts_with_clear_button = QPushButton("Clear")
        starts_with_clear_button.clicked.connect(lambda: self.starts_with_clear())
        col = 2
        grid.addWidget(starts_with_clear_button, row, col)

        row += 1
        col = 0
        grid.addWidget(QLabel("Ends with:"), row, col)
        self.ends_with = QLineEdit()
        self.ends_with.setToolTip(ENDS_WITH_TOOLTIP)
        col = 1
        grid.addWidget(self.ends_with, row, col)
        ends_with_clear_button = QPushButton("Clear")
        ends_with_clear_button.clicked.connect(lambda: self.ends_with_clear())
        col = 2
        grid.addWidget(ends_with_clear_button, row, col)

        row += 1
        col = 0
        grid.addWidget(QLabel("Number of Letters:"), row, col)
        self.number_of_letters = QLineEdit()
        self.number_of_letters.setDisabled(True)
        self.number_of_letters.setToolTip(NUMBER_OF_LETTERS_TOOLTIP)
        col = 1
        grid.addWidget(self.number_of_letters, row, col)
        self.number_of_letters_clear_button = QPushButton("Clear")
        self.number_of_letters_clear_button.setDisabled(True)
        self.number_of_letters_clear_button.clicked.connect(lambda: self.number_of_letters_clear())
        col = 2
        grid.addWidget(self.number_of_letters_clear_button, row, col)

        row += 1
        col = 0
        grid.addWidget(QLabel("Dictionary:"), row, col)
        self.dictionary = QComboBox()
        self.dictionary.addItems([name.name for name in DictionaryName])
        self.dictionary.setCurrentIndex(DictionaryName.COLLINS.value)
        col = 1
        grid.addWidget(self.dictionary, row, col)

        row += 1
        col = 1
        self.progress_bar = QProgressBar()
        self.progress_bar.setDisabled(True)
        grid.addWidget(self.progress_bar, row, col)

        return grid

    def build_buttons(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.search_for_words)
        self.submit_button.setShortcut(QKeySequence(Qt.Key_Return))
        layout.addWidget(self.submit_button)
        self.clear_all_button = QPushButton("Clear")
        self.clear_all_button.clicked.connect(self.clear_all)
        layout.addWidget(self.clear_all_button)
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        self.exit_button.setShortcut(QKeySequence(Qt.Key_Escape))
        layout.addWidget(self.exit_button)

        return layout

    def search_for_words(self):
        data = self.validate_input_data()

        if data is None:
            return

        self.word_searcher = WordSearcher(data)
        self.thread = QThread()
        self.word_searcher.intReady.connect(self.on_count_changed)
        self.word_searcher.moveToThread(self.thread)
        self.word_searcher.finished.connect(self.thread_finished)
        self.thread.started.connect(self.word_searcher.get_words)
        self.progress_bar.setDisabled(False)
        self.thread.start()

    def on_count_changed(self, value):
        self.progress_bar.setValue(value)

    def thread_finished(self, words: List[CustomWord]) -> None:
        self.thread.quit()
        self.progress_bar.setValue(100)
        word_sort = sorted(words, key=attrgetter('word'))
        value_sort = sorted(word_sort, key=attrgetter('value'), reverse=True)
        dictionary_definitions = "DEFINE" in self.get_dictionary_name().name
        is_scrabble = self.get_type_of_game() == TypeOfGame.SCRABBLE
        FoundWords(value_sort, dictionary_definitions, is_scrabble)

    def validate_input_data(self):
        data = InputDataBuilder(self.available_letters.text()) \
                .game_type(self.get_type_of_game()) \
                .contains(self.contains_letters.text()) \
                .starts_with(self.starts_with.text()) \
                .ends_with(self.ends_with.text()) \
                .dictionary_name(self.get_dictionary_name()) \
                .number_of_letters(self.number_of_letters.text()) \
                .build()
        validator = Validator(data)
        errors = validator.validate()

        if len(errors) > 0:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Please fix these errors")
            dlg.setText('\n'.join(errors))
            dlg.exec()

            return None

        return data

    def ends_with_clear(self):
        self.ends_with.clear()
        self.ends_with.setFocus()

    def starts_with_clear(self):
        self.starts_with.clear()
        self.starts_with.setFocus()

    def contains_letters_clear(self):
        self.contains_letters.clear()
        self.contains_letters.setFocus()

    def available_letters_clear(self):
        self.available_letters.clear()
        self.available_letters.setFocus()

    def number_of_letters_clear(self):
        self.number_of_letters.clear()
        self.number_of_letters.setFocus()

    def clear_all(self):
        self.available_letters.clear()
        self.contains_letters.clear()
        self.starts_with.clear()
        self.ends_with.clear()

        if self.get_type_of_game() != TypeOfGame.WORDLE:
            self.number_of_letters.clear()

        self.available_letters.setFocus()

    def get_type_of_game(self) -> TypeOfGame:
        type_of_game = TypeOfGame.SCRABBLE
        selected = [button.text() for button in self.radio_group.buttons() if button.isChecked()]

        if len(selected) > 0:
            selected_text = selected[0].upper()

            for element in TypeOfGame:
                if element.name == selected_text:
                    type_of_game = element
                    break

        return type_of_game

    def get_dictionary_name(self) -> DictionaryName:
        dictionary_name = DictionaryName.COLLINS

        for name in DictionaryName:
            if name.name == self.dictionary.currentText():
                dictionary_name = name
                break

        return dictionary_name

    def radio_button_changed(self, btn):
        if btn.text().upper() == TypeOfGame.SCRABBLE.name:
            self.number_of_letters.clear()
            self.number_of_letters.setDisabled(True)
            self.number_of_letters_clear_button.setDisabled(True)
            self.available_letters.setDisabled(False)
            self.available_letters_clear_button.setDisabled(False)
            self.available_letters_label.setText(AVAILABLE_LETTERS_TEXT)
            self.available_letters.setToolTip(AVAILABLE_LETTERS_TOOLTIP)
        elif btn.text().upper() == TypeOfGame.CROSSWORD.name:
            self.number_of_letters.clear()
            self.number_of_letters.setDisabled(False)
            self.number_of_letters_clear_button.setDisabled(False)
            self.available_letters.setDisabled(True)
            self.available_letters_clear_button.setDisabled(True)
            self.available_letters.clear()
        elif btn.text().upper() == TypeOfGame.WORDLE.name:
            self.number_of_letters.setText("5")
            self.number_of_letters.setDisabled(False)
            self.number_of_letters_clear_button.setDisabled(False)
            self.available_letters.setDisabled(False)
            self.available_letters_clear_button.setDisabled(False)
            self.available_letters_label.setText(CANT_HAVE_LETTERS_TEXT)
            self.available_letters.setToolTip(CANT_HAVE_LETTERS_TOOLTIP)
