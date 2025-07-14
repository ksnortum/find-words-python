import logging

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit

from utils.utils import get_string_from_file
from view.button import ok_button


class DisplayHtml(QDialog):
    def __init__(self, file_name: str, title: str, width: int, height: int):
        super().__init__()
        self.file_name = file_name
        self.title = title
        self.dialog_width = width
        self.dialog_height = height

    def display(self):
        logging.debug('in display()')
        self.setWindowTitle(self.title)
        css = get_string_from_file("html/app.css")
        self.setStyleSheet(css)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        about_widget = QTextEdit()
        about_widget.setMinimumSize(self.dialog_width, self.dialog_height)
        about_widget.setReadOnly(True)
        about_widget.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse |
                                             Qt.TextInteractionFlag.TextBrowserInteraction)
        about_widget.setHtml(get_string_from_file(self.file_name))
        main_layout.addWidget(about_widget)
        main_layout.addLayout(ok_button(self))

        self.show()
        self.exec()
