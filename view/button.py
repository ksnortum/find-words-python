from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QPushButton


def ok_button(self) -> QHBoxLayout:
    """Return an OK button in an HBox"""
    button_layout = QHBoxLayout()
    button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
    button = QPushButton("OK")
    button.clicked.connect(self.close)
    button_layout.addWidget(button)

    return button_layout
