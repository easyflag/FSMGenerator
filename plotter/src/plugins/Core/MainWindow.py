from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QTabWidget,
    QSizePolicy,
    QGraphicsView,
    QGraphicsScene,
)

from libs.ActionSystem.ActionContainer import TabContainer

from plugins.Core.FSMNodeItem import FSMNodeItem,EventItem

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

        view = QGraphicsView(centralWidget)
        vLayout.addWidget(view)

        self.__scene = QGraphicsScene(centralWidget)
        self.__scene.sceneRectChanged.connect(lambda rec: print(rec))
        view.setScene(self.__scene)
        self.__scene.addEllipse(0, 0, 100, 60)
        self.__scene.addItem(FSMNodeItem())
        self.__scene.addItem(EventItem())

        self.show()
