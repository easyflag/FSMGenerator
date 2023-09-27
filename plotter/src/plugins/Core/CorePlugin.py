from libs.PluginManage.IPlugin import IPlugin


class CorePlugin(IPlugin):
    def __init__(self) -> None:
        super().__init__()

    def initialize(self):
        print("CorePlugin initialize")