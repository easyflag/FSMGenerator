from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QTableWidget

from libs.ActionSystem.ActionGroup import TabGroup


class ActionContainer:
    def registerActionGroup(self, groupId, title="", icon=QIcon()):
        pass

    def unregisterActionGroup(self, groupId):
        pass

    def actionGroup(self, groupId):
        pass


class TabContainer(ActionContainer):
    def __init__(self, tabWidget):
        super().__init__()

        self.__groups = {}
        self.__tabWidget = tabWidget

    def registerActionGroup(self, groupId, title="", icon=QIcon()):
        if groupId in self.__groups:
            return self.__groups[groupId]

        group = TabGroup()
        self.__tabWidget.addTab(group.page(), icon, title)
        self.__groups[groupId] = group

        return group

    def unregisterActionGroup(self, groupId):
        if not groupId in self.__groups:
            return

        group = self.__groups.pop(groupId)
        i = self.__tabWidget.indexOf(group.page())
        self.__tabWidget.removeTab(i)

    def actionGroup(self, groupId):
        if not groupId in self.__groups:
            return None

        return self.__groups[groupId]
