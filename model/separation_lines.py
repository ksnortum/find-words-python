from PyQt5 import QtWidgets


class QHSeparationLine(QtWidgets.QFrame):
    """
    a horizontal separation line\n
    """

    def __init__(self, height: int=2):
        super().__init__()
        self.setMinimumWidth(1)
        self.setFixedHeight(max(height, 2))
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        return


class QVSeparationLine(QtWidgets.QFrame):
    """
    a vertical separation line\n
    """

    def __init__(self, width: int=2):
        super().__init__()
        self.setFixedWidth(max(width, 2))
        self.setMinimumHeight(1)
        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        return
