from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsTextItem,
    QMenu,
    QGraphicsSceneContextMenuEvent,
)
from PySide6.QtCore import Qt, QRectF


class EventItem(QGraphicsItem):
    def __init__(self, parentItem: QGraphicsItem = None) -> None:
        super().__init__(parentItem)

        self.__frameItem = QGraphicsRectItem(0, 0, 100, 60, self)

        self.__titleItem = QGraphicsTextItem("entry", self.__frameItem)
        self.__titleItem.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextEditorInteraction)

        self.__contentItem = QGraphicsTextItem(
            "do somothing.", self.__frameItem)
        self.__titleItem.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextEditorInteraction)
        self.__contentItem.setPos(0, 20)

    def boundingRect(self):
        return QRectF(0, 0, 100, 60)

    def paint(self, painter, option, widget):
        pass


class FSMNodeItem(QGraphicsItem):
    def __init__(self) -> None:
        super().__init__()

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.__headerItem = QGraphicsRectItem(0, 0, 100, 20, self)

        self.__titleItem = QGraphicsTextItem("MyItem", self.__headerItem)
        self.__titleItem.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextEditorInteraction
        )

        self.__bottomItem = QGraphicsRectItem(0, 0, 100, 80, self)
        self.__bottomItem.setPos(0, 20)

        self.__menu = QMenu()
        self.__menu.addAction("add entry handle", lambda: self.__addEventEditor())

    def boundingRect(self):
        return QRectF(0, 0, 100, 100)

    def paint(self, painter, option, widget):
        pass

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent):
        self.__menu.exec(event.screenPos())

    def __addEventEditor(self):
        e = EventItem(self)
        e.setPos(0, 20)
