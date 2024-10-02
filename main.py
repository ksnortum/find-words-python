import logging
import sys

from PyQt6.QtWidgets import QApplication
from view.main_window import MainWindow
from utils.utils import get_string_from_file


def main():
    logging.basicConfig(format='%(levelname)s %(message)s', level=logging.WARN)
    app = QApplication(sys.argv)
    css = get_string_from_file("html/app.css")
    app.setStyleSheet(css)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
