from PySide6.QtWidgets import *

from libs.ActionSystem.ActionContainer import TabContainer

from plugins.Core.GraphicsView import *
from plugins.Core.GraphicsScene import *
from plugins.Core.FSMNodeItem import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__actionContainer = None
        self.__scene = None

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
        group = self.__actionContainer.registerActionGroup(1, "test")
        group.registerAction(1, "test")

        view = GraphicsView(centralWidget)
        vLayout.addWidget(view)

        self.__scene = GraphicsScene(centralWidget)
        # self.__scene.sceneRectChanged.connect(lambda rec: print(rec))
        view.setScene(self.__scene)

        self.__scene.addItem(FSMNodeItem_())
        self.__scene.addItem(FSMNodeItem())

        self.show()
