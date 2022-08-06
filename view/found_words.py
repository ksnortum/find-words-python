from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout, QDialog, QLabel, QMessageBox, QScrollArea, QFrame

from model.custom_word import CustomWord
from view.button import ok_button


class FoundWords(QDialog):
    def __init__(self, words: List[CustomWord]) -> None:
        super().__init__()
        self.words = words

        if len(words) == 0:
            self.nothing_found()
            return

        self.build_gui()
        self.exec()

    def build_gui(self):
        self.setWindowTitle("Found")
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
            word_label = QLabel(word.get_word())
            word_label.setStyleSheet("background-color: white;")
            word_label.setAlignment(Qt.AlignCenter)
            grid.addWidget(word_label, row, 0)
            value_label = QLabel(str(word.get_value()))
            value_label.setAlignment(Qt.AlignCenter)
            value_label.setStyleSheet("background-color: white;")
            grid.addWidget(value_label, row, 1)
            row += 1

        main_layout.addWidget(scroll)
        main_layout.addLayout(ok_button(self))

    @staticmethod
    def nothing_found() -> None:
        dlg = QMessageBox()
        dlg.setWindowTitle("Notice")
        dlg.setText("No matching words were found")
        dlg.exec()
