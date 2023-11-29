from PySide6.QtCore import QObject, QSize, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSizePolicy, QToolButton


class Action(QObject):
    class State:
        Idle = 0
        Running = 1
        Disabled = 2

    triggered = Signal()

    def __init__(self):
        super().__init__()


class TabAction(Action):
    def __init__(self, title="", icon=QIcon()):
        super().__init__()

        self.__button = QToolButton()
        self.__button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.__button.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding
        )
        self.__button.setIconSize(QSize(40, 40))
        self.__button.setText(title)
        self.__button.setIcon(icon)

        self.__button.clicked.connect(self.triggered)

    def button(self):
        return self.__button
