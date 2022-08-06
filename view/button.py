from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QPushButton


def ok_button(self) -> QHBoxLayout:
    button_layout = QHBoxLayout()
    button_layout.setAlignment(Qt.AlignRight)
    button = QPushButton("OK")
    button.clicked.connect(self.close)
    button_layout.addWidget(button)

    return button_layout
