from PyQt6 import QtWidgets


class QHSeparationLine(QtWidgets.QFrame):
    """A horizontal separation line"""
    def __init__(self, height: int = 2):
        super().__init__()
        self.setMinimumWidth(1)
        self.setFixedHeight(max(height, 2))
        self.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Minimum)
        return


class QVSeparationLine(QtWidgets.QFrame):
    """A vertical separation line."""
    def __init__(self, width: int = 2):
        super().__init__()
        self.setFixedWidth(max(width, 2))
        self.setMinimumHeight(1)
        self.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        return
