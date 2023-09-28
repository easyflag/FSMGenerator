from libs.ExtensionSystem.IPlugin import IPlugin
from plugins.Core.MainWindow import MainWindow


class CorePlugin(IPlugin):
    def __init__(self) -> None:
        super().__init__()

        self.__mainWin = MainWindow()

    def initialize(self):
        print("CorePlugin initialize")

        self.__mainWin.initialize()