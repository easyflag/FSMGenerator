from enum import Enum
from typing import Any
import math

from PySide6.QtGui import QFontMetrics, QFont
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsSceneMouseEvent,
    QGraphicsTextItem,
    QMenu,
    QGraphicsSceneContextMenuEvent
)
from PySide6.QtCore import Qt, QRectF


class MyTextItem(QGraphicsTextItem):
    def __init__(self):
        super().__init__()
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.setPlainText("123")

        self.xChanged.connect(lambda: print("xChanged"))
        self.widthChanged.connect(lambda: print("widthChanged"))

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        # print(change, value)

        return super().itemChange(change, value)


class FSMNodeItem(QGraphicsRectItem):
    class TitleItem(QGraphicsRectItem):
        def __init__(self, parentItem: QGraphicsItem):
            super().__init__(parentItem)

            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

            self.setRect(0, 0, 100, 20)

            self.__txt = "State"
            self.__canDrawTxt = True
            self.__font = QFont()
            self.__margin = 4

            self.__inputItem = None

            self.__resize()

        def paint(self, painter, option, widget):
            super().paint(painter, option, widget)

            if self.__canDrawTxt:
                painter.setFont(self.__font)
                painter.drawText(self.rect(),
                                 Qt.TextFlag.TextWrapAnywhere | Qt.AlignmentFlag.AlignCenter,
                                 self.__txt)

        def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
            if not self.__inputItem:
                self.__inputItem = QGraphicsTextItem(self.__txt, self)
                self.__inputItem.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
                self.__inputItem.setTextWidth(self.rect().width())

                self.__canDrawTxt = False
                self.update()

            return super().mouseDoubleClickEvent(event)

        def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any):
            if change == QGraphicsItem.GraphicsItemChange.ItemSelectedHasChanged and value == 0:
                if self.__inputItem:
                    self.__txt = self.__inputItem.toPlainText()
                    self.__canDrawTxt = True
                    self.update()

                    self.__resize()

                    self.scene().removeItem(self.__inputItem)
                    self.__inputItem = None

            return super().itemChange(change, value)

        def __resize(self):
            m = QFontMetrics(self.__font)
            txtW = m.horizontalAdvance(self.__txt)
            txtH = m.height()
            rectW = self.rect().width()

            lines = txtW / rectW
            lines = math.ceil(lines)
            self.setRect(0, 0, rectW, txtH * lines + self.__margin * 2)

    class EventItem(QGraphicsItem):
        class EventType(Enum):
            Entry = 1
            Exit = 2
            Custom = 3

        def __init__(self, eventType: EventType, parentItem: QGraphicsItem):
            super().__init__(parentItem)

            self.__eventType = eventType

            self.__frameItem = QGraphicsRectItem(0, 0, 100, 60, self)

            self.__titleItem = QGraphicsTextItem("entry", self.__frameItem)

            if self.__eventType == self.EventType.Entry:
                self.__titleItem.setPlainText("entry")
            elif self.__eventType == self.EventType.Exit:
                self.__titleItem.setPlainText("exit")
            elif self.__eventType == self.EventType.Custom:
                self.__titleItem.setPlainText("custom")
                self.__titleItem.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)

            self.__contentItem = QGraphicsTextItem("do somothing.", self.__frameItem)
            self.__contentItem.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
            self.__contentItem.setPos(0, 20)

        @property
        def eventType(self):
            return self.__eventType

        def boundingRect(self):
            return QRectF(0, 0, 100, 60)

        def paint(self, painter, option, widget):
            pass

    def __init__(self, parentItem: QGraphicsItem = None) -> None:
        super().__init__(parentItem)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.__headerItem = self.TitleItem(self)

        self.__eventItems = []

        self.__menu = QMenu()
        self.__menu.addAction("add entry event", lambda: self.__addEventEditor(self.EventItem.EventType.Entry))
        self.__menu.addAction("add exit event", lambda: self.__addEventEditor(self.EventItem.EventType.Exit))
        self.__menu.addAction("add custom event", lambda: self.__addEventEditor(self.EventItem.EventType.Custom))
        self.__menu.addAction("remove entry event", lambda: self.__removeEventEditor(self.EventItem.EventType.Entry))
        self.__menu.addAction("remove exit event", lambda: self.__removeEventEditor(self.EventItem.EventType.Exit))
        self.__menu.addAction("remove custom event", lambda: self.__removeEventEditor(self.EventItem.EventType.Custom))
        self.__menu.addAction("s", lambda: self.setScale(1.5))

        self.__relayout()

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent):
        self.__menu.exec(event.screenPos())

    def __resort(self):
        self.__eventItems.sort(key=lambda item: item.eventType.value)

    def __relayout(self):
        totalH = self.__headerItem.boundingRect().height()
        for item in self.__eventItems:
            totalH += item.boundingRect().height()
        if totalH < 80:
            totalH = 80
        self.setRect(0, 0, 100, totalH)

        y = self.__headerItem.boundingRect().height()
        for item in self.__eventItems:
            item.setPos(0, y)
            y += item.boundingRect().height()

    def __addEventEditor(self, eventType: EventItem.EventType):
        item = self.EventItem(eventType, self)
        item.setPos(0, 20)
        self.__eventItems.append(item)

        self.__resort()
        self.__relayout()

    def __removeEventEditor(self, eventType: EventItem.EventType):
        for item in self.__eventItems:
            if item.eventType == eventType:
                self.__eventItems.remove(item)
                self.scene().removeItem(item)
                break

        self.__relayout()
