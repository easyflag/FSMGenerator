from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QSizePolicy

from libs.ActionSystem.ActionContainer import TabContainer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__actionContainer = None

    def initialize(self):
        self.resize(800, 600)

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        vLayout = QVBoxLayout()
        vLayout.setSpacing(0)
        vLayout.setContentsMargins(0, 0, 0, 0)
        centralWidget.setLayout(vLayout)

        tab = QTabWidget(centralWidget)
        tab.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        tab.setMinimumSize(0, 100)
        vLayout.addWidget(tab)

        self.__actionContainer = TabContainer(tab)

        self.show()
