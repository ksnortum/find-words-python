import logging
import sys

from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow


def main():
    logging.basicConfig(format='%(levelname)s %(message)s', level=logging.DEBUG)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
