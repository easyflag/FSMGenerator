from PySide6.QtWidgets import *
from PySide6.QtCore import *


class GraphicsView(QGraphicsView):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.__anchorPos = QPointF()
        self.__panMode = False

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.RightButton:
            return super().mousePressEvent(event)
                    
        self.__panMode = True
        self.__anchorPos = event.pos()
        self.setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        if event.button() != Qt.MouseButton.RightButton:
            return super().mouseReleaseEvent(event)
                    
        self.__panMode = False
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def mouseMoveEvent(self, event):
        if not self.__panMode:
            return super().mouseMoveEvent(event)
        
        hBar = self.horizontalScrollBar()
        vBar = self.verticalScrollBar()
        d = event.pos() - self.__anchorPos
        hBar.setValue(hBar.value() - d.x())
        vBar.setValue(vBar.value() - d.y())
        self.__anchorPos = event.pos()
        
    def wheelEvent(self, event):
        s = event.angleDelta().y() / 1200 + 1
        self.scale(s, s)

        return super().wheelEvent(event)
