import logging

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit

from utils.utils import get_string_from_file
from view.button import ok_button


class AboutPage(QDialog):
    def __init__(self):
        super().__init__()
        logging.debug('in AboutPage')

    # TODO, finish -- size correctly?
    def display(self):
        logging.debug('in display()')
        self.setWindowTitle("About")
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        about_widget = QTextEdit()
        about_widget.setReadOnly(True)
        about_widget.setStyleSheet(  # TODO does this work?
            'h1 {'
            '   background-color: #d0d0d0;'
            '   border-radius: 5px;'
            '}'
        )
        about_widget.setHtml(get_string_from_file("html/about.html"))
        main_layout.addWidget(about_widget)
        main_layout.addLayout(ok_button(self))

        self.show()
        self.exec()
