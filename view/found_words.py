from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout, QVBoxLayout, QDialog, QLabel, QMessageBox, QScrollArea, QFrame

from model.custom_word import CustomWord
from view.button import ok_button


class FoundWords(QDialog):
    """
    Build a dialog window to display the words found by the search.
    """
    def __init__(self, words: list[CustomWord], dictionary_definitions: bool, is_scrabble: bool) -> None:
        super().__init__()
        self.words = words
        self.dictionary_definitions = dictionary_definitions
        self.is_scrabble = is_scrabble

        if len(words) == 0:
            self.nothing_found()
            return

        self.build_gui()
        self.exec()

    def build_gui(self):
        self.setWindowTitle("Found Words")
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Set up a scrollable area for the grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        inner = QFrame(scroll)
        grid = QGridLayout()
        inner.setLayout(grid)
        scroll.setWidget(inner)

        # Loop through words placing them in a grid
        row = 0
        for word in self.words:
            col = 0
            word_label = QLabel(word.get_word())
            word_label.setStyleSheet("background-color: white;")
            word_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            grid.addWidget(word_label, row, col)
            col += 1

            if self.is_scrabble:
                value_label = QLabel(str(word.get_value()))
                value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                value_label.setStyleSheet("background-color: white;")
                grid.addWidget(value_label, row, col)
                col += 1

            if self.dictionary_definitions:
                definition_label = QLabel(word.get_definition())
                definition_label.setStyleSheet("background-color: white;")
                grid.addWidget(definition_label, row, col)
                col += 1

            row += 1

        main_layout.addWidget(scroll)
        main_layout.addLayout(ok_button(self))

    @staticmethod
    def nothing_found() -> None:
        dlg = QMessageBox()
        dlg.setWindowTitle("Notice")
        dlg.setText("No matching words were found")
        dlg.exec()
