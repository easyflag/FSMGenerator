from enum import Enum
from typing import Any
import math

from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *


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


class FSMNodeItem_(QGraphicsRectItem):
    class TitleItem(QGraphicsRectItem):
        def __init__(self, parentItem: QGraphicsItem):
            super().__init__(parentItem)

            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
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

            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

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

    def mousePressEvent(self, event):
        print("FSMNodeItem_", event, event.isAccepted())
        return super().mousePressEvent(event)


class FSMNode(QGraphicsProxyWidget):
    def __init__(self):
        super().__init__()

        self.__anchorPos = QPointF(0, 0)

        f = QFrame()
        f.setFrameShape(QFrame.Shape.Box)
        f.setFrameShadow(QFrame.Shadow.Raised)

        vBox = QVBoxLayout()
        vBox.setContentsMargins(1, 1, 1, 1)
        f.setLayout(vBox)

        le = QLineEdit("Node1")
        le.setAlignment(Qt.AlignmentFlag.AlignCenter)
        le.setFrame(False)
        le.setStyleSheet("QLineEdit{ background: lightblue; }")
        vBox.addWidget(le)

        hBox = QHBoxLayout()
        vBox.addLayout(hBox)

        self.__lw = QListWidget()
        self.__lw.setMaximumWidth(80)
        # self.__lw.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        hBox.addWidget(self.__lw)
        self.__te = QTextEdit()
        # self.__te.setFrameShape(QFrame.Shape.NoFrame)
        hBox.addWidget(self.__te)

        # t = QTabWidget()
        # t.setTabsClosable(True)
        # t.addTab(QTextEdit(), "")
        # t.addTab(QTextEdit(), "")
        # vBox.addWidget(t)

        self.setWidget(f)

        self.addTab("entry")
        self.addTab("exit")

        self.setGeometry(0, 0, 300, 300)

    def addTab(self, title):
        item = QListWidgetItem(title)
        item.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
        self.__lw.addItem(item)

    def mousePressEvent(self, event):
        self.__anchorPos = event.pos()

    def mouseMoveEvent(self, event):
        p = event.scenePos() - self.__anchorPos
        self.setPos(p)


class FSMDragHandle(QGraphicsEllipseItem):
    def __init__(self, parentItem: QGraphicsItem = None):
        super().__init__(parentItem)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        
        self.setBrush(Qt.GlobalColor.white)
        
        self.__mouseMoveCB = None

    def setMouseMoveCB(self, mouseMoveCB):
        self.__mouseMoveCB = mouseMoveCB

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        print("FSMDragHandle mouseMoveEvent", event)
        if self.__mouseMoveCB:
            c = self.rect().center()
            p = self.mapToParent(c)
            self.__mouseMoveCB(p)
        return super().mouseMoveEvent(event)


class FSMLinkLine(QGraphicsLineItem):
    def __init__(self):
        super().__init__()

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        # self.setHandlesChildEvents(True)
        self.setLine(0, 0, 50, 50)

        self.__headDragHandle = FSMDragHandle(self)
        self.__headDragHandle.setMouseMoveCB(lambda pos: self.__handleDragHandleMove(pos, True))
        # self.__headDragHandle.setVisible(False)
        p1 = self.line().p1()
        self.__headDragHandle.setRect(p1.x() - 2, p1.y() - 2, 4, 4)

        self.__tailDragHandle = FSMDragHandle(self)
        self.__tailDragHandle.setMouseMoveCB(lambda pos: self.__handleDragHandleMove(pos, False))
        # self.__headDragHandle.setVisible(False)
        p2 = self.line().p2()
        self.__tailDragHandle.setRect(p2.x() - 2, p2.y() - 2, 4, 4)

    def __handleDragHandleMove(self, pos: QPointF, isHead: bool):
        if isHead:
            tail = self.line().p2()
            self.setLine(pos.x(), pos.y(), tail.x(), tail.y())
        else:
            head = self.line().p1()
            self.setLine(head.x(), head.y(), pos.x(), pos.y())

    # def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value: Any):
    #     if change == QGraphicsItem.GraphicsItemChange.ItemSelectedHasChanged:
    #         if value:
    #             self.__headDragHandle.setVisible(True)
    #         else:
    #             self.__headDragHandle.setVisible(False)

    #     return super().itemChange(change, value)

    def mouseMoveEvent(self, event):
        print(self.line(), self.scenePos())
        return super().mouseMoveEvent(event)
