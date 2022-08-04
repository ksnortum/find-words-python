import logging

from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QFont
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
)

from controller.word_searcher import WordSearcher
from model.dictionary_name import DictionaryName
from model.input_data import InputDataBuilder
from model.type_of_game import TypeOfGame
from controller.validator import Validator

AVAILABLE_LETTERS_TEXT = "Available Letters:"
CANT_HAVE_LETTERS_TEXT = "Can't Have Letters:"


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
        self.number_of_letters_clear = None
        self.build_gui()

    def build_gui(self):
        logging.debug("building GUI")
        self.setWindowTitle("Find Words")
        self.setContentsMargins(20, 20, 20, 20)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        main_layout.addWidget(self.build_title())
        main_layout.addLayout(self.build_radio_buttons())
        main_layout.addLayout(self.build_grid())
        main_layout.addLayout(self.build_buttons())

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
        col = 1
        grid.addWidget(self.available_letters, row, col)
        available_letters_clear = QPushButton("Clear")
        available_letters_clear.clicked.connect(lambda: self.available_letters.clear())
        col = 2
        grid.addWidget(available_letters_clear, row, col)

        row += 1
        col = 0
        grid.addWidget(QLabel("Contains Letters:"), row, col)
        self.contains_letters = QLineEdit()
        col = 1
        grid.addWidget(self.contains_letters, row, col)
        contains_letters_clear = QPushButton("Clear")
        contains_letters_clear.clicked.connect(lambda: self.contains_letters.clear())
        col = 2
        grid.addWidget(contains_letters_clear, row, col)

        row += 1
        col = 0
        grid.addWidget(QLabel("Starts with:"), row, col)
        self.starts_with = QLineEdit()
        col = 1
        grid.addWidget(self.starts_with, row, col)
        starts_with_clear = QPushButton("Clear")
        starts_with_clear.clicked.connect(lambda: self.starts_with.clear())
        col = 2
        grid.addWidget(starts_with_clear, row, col)

        row += 1
        col = 0
        grid.addWidget(QLabel("Ends with:"), row, col)
        self.ends_with = QLineEdit()
        col = 1
        grid.addWidget(self.ends_with, row, col)
        ends_with_clear = QPushButton("Clear")
        ends_with_clear.clicked.connect(lambda: self.ends_with.clear())
        col = 2
        grid.addWidget(ends_with_clear, row, col)

        row += 1
        col = 0
        grid.addWidget(QLabel("Number of Letters"), row, col)
        self.number_of_letters = QLineEdit()
        self.number_of_letters.setDisabled(True)
        col = 1
        grid.addWidget(self.number_of_letters, row, col)
        self.number_of_letters_clear = QPushButton("Clear")
        self.number_of_letters_clear.setDisabled(True)
        self.number_of_letters_clear.clicked.connect(lambda: self.number_of_letters.clear())
        col = 2
        grid.addWidget(self.number_of_letters_clear, row, col)

        row += 1
        col = 0
        grid.addWidget(QLabel("Dictionary"), row, col)
        self.dictionary = QComboBox()
        self.dictionary.addItems([name.name for name in DictionaryName])
        col = 1
        grid.addWidget(self.dictionary, row, col)

        row += 1
        col = 1
        self.progress_bar = QProgressBar()
        # TODO self.progress_bar.hide()
        grid.addWidget(self.progress_bar, row, col)

        return grid

    def build_buttons(self):
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignRight)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.search_for_words)
        layout.addWidget(self.submit_button)
        self.clear_all_button = QPushButton("Clear")
        self.clear_all_button.clicked.connect(self.clear_all)
        layout.addWidget(self.clear_all_button)
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.close)
        layout.addWidget(self.exit_button)

        return layout

    # TODO finish: get words from thread and display
    def search_for_words(self):
        data = self.validate_input_data()

        if data is None:
            return

        self.word_searcher = WordSearcher(data)
        self.thread = QThread()
        self.word_searcher.intReady.connect(self.on_count_changed)
        self.word_searcher.moveToThread(self.thread)
        self.word_searcher.finished.connect(self.thread.quit)
        self.word_searcher.finished.connect(lambda: self.progress_bar.setValue(100))
        self.thread.started.connect(self.word_searcher.get_words)
        self.progress_bar.show()
        self.thread.start()

    def on_count_changed(self, value):
        self.progress_bar.setValue(value)

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
        dictionary_name = DictionaryName.OSPD

        for name in DictionaryName:
            if name == self.dictionary.currentText():
                dictionary_name = name
                break

        return dictionary_name

    def radio_button_changed(self, btn):
        if btn.text().upper() == TypeOfGame.SCRABBLE.name:
            self.number_of_letters.clear()
            self.number_of_letters.setDisabled(True)
            self.number_of_letters_clear.setDisabled(True)
            self.available_letters_label.setText(AVAILABLE_LETTERS_TEXT)
        elif btn.text().upper() == TypeOfGame.CROSSWORD.name:
            self.number_of_letters.clear()
            self.number_of_letters.setDisabled(False)
            self.number_of_letters_clear.setDisabled(False)
            self.available_letters_label.setText(AVAILABLE_LETTERS_TEXT)
        elif btn.text().upper() == TypeOfGame.WORDLE.name:
            self.number_of_letters.setText("5")
            self.number_of_letters.setDisabled(False)
            self.number_of_letters_clear.setDisabled(False)
            self.available_letters_label.setText(CANT_HAVE_LETTERS_TEXT)
