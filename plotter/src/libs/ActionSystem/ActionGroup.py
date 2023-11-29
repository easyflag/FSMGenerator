from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QSpacerItem

from libs.ActionSystem.Action import TabAction


class ActionGroup:
    def registerActionGroup(self, groupId, title="", icon=QIcon()):
        pass

    def registerAction(self, actionId, title="", icon=QIcon()):
        pass

    def unregisterActionGroup(self, groupId):
        pass

    def unregisterAction(self, actionId):
        pass

    def actionGroup(self, groupId):
        pass

    def action(self, actionId):
        pass


class TabGroup(ActionGroup):
    def __init__(self):
        super().__init__()

        self.__groups = {}
        self.__actions = {}

        self.__page = QWidget()
        self.__page.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.__hLayout = QHBoxLayout(self.__page)
        spacer = QSpacerItem(
            1, 1, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.__hLayout.addSpacerItem(spacer)

    def registerActionGroup(self, groupId, title="", icon=QIcon()):
        # TODO
        return None

    def registerAction(self, actionId, title="", icon=QIcon()):
        if actionId in self.__actions:
            return self.__actions[actionId]

        action = TabAction(title, icon)

        c = self.__hLayout.count()
        self.__hLayout.insertWidget(c - 1, action.button())
        self.__actions[actionId] = action

        return action

    def unregisterActionGroup(self, groupId):
        # TODO
        return None

    def unregisterAction(self, actionId):
        if not actionId in self.__actions:
            return

        action = self.__actions.pop(actionId)
        self.__hLayout.removeWidget(action.button())

    def actionGroup(self, groupId):
        if not groupId in self.__groups:
            return None

        return self.__groups[groupId]

    def action(self, actionId):
        if not actionId in self.__actions:
            return None

        return self.__actions[actionId]

    def page(self):
        return self.__page
