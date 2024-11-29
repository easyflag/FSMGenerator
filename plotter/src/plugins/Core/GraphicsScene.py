from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class GraphicsScene(QGraphicsScene):
    D = 24

    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        left = self.sceneRect().left()
        right = self.sceneRect().right()
        top = self.sceneRect().top()
        bottom = self.sceneRect().bottom()
        
        n = left // GraphicsScene.D - 2
        left = GraphicsScene.D * n
        n = right // GraphicsScene.D + 3
        right = GraphicsScene.D * n
        n = top // GraphicsScene.D - 2
        top = GraphicsScene.D * n
        n = bottom // GraphicsScene.D + 3
        bottom = GraphicsScene.D * n

        pen = QPen()
        pen.setColor(QColor(60, 60, 60, 30))
        pen.setWidth(0)
        pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(pen)

        # draw horizental lines
        i = 0
        while i >= top:
            painter.drawLine(left, i, right, i)
            i -= 24
        i = 0
        while i <= bottom:
            painter.drawLine(left, i, right, i)
            i += 24

        # draw vertical lines
        i = 0
        while i <= right:
            painter.drawLine(i, top, i, bottom)
            i += 24
        i = 0
        while i >= left:
            painter.drawLine(i, top, i, bottom)
            i -= 24
