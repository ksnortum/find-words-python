import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit

from utils.utils import get_string_from_file
from view.button import ok_button


class DisplayHtml(QDialog):
    def __init__(self, file_name, title, width, height):
        super().__init__()
        self.file_name = file_name
        self.title = title
        self.width = width
        self.height = height

    def display(self):
        logging.debug('in display()')
        self.setWindowTitle(self.title)
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        about_widget = QTextEdit()
        about_widget.setMinimumSize(self.width, self.height)
        about_widget.setReadOnly(True)
        about_widget.setTextInteractionFlags(Qt.LinksAccessibleByMouse | Qt.TextBrowserInteraction)
        about_widget.setHtml(get_string_from_file(self.file_name))
        main_layout.addWidget(about_widget)
        main_layout.addLayout(ok_button(self))

        self.show()
        self.exec()
