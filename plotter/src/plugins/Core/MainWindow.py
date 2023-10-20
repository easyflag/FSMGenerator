from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QGraphicsView
from PySide2.QtWidgets import QGraphicsScene
from PySide2.QtWidgets import QGraphicsRectItem
from PySide2.QtWidgets import QGraphicsItem
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.view = None
        # self.scene = None

    def initialize(self):
        self.resize(800, 600)

        cWidget = QWidget()
        self.setCentralWidget(cWidget)

        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        cWidget.setLayout(vbox)

        view = QGraphicsView(cWidget)
        vbox.addWidget(view)

        scene = QGraphicsScene()
        scene.setBackgroundBrush(Qt.red)
        view.setScene(scene)

        rect = QGraphicsRectItem()
        rect.setRect(0, 0, 100, 60)
        rect.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        scene.addItem(rect)

        self.show()
