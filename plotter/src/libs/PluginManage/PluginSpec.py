import importlib


class PluginSpec():
    def __init__(self) -> None:
        self.__name = ''
        self.__plugin = None

    @property
    def name(self):
        return self.__name

    def _load(self):
        module = importlib.import_module(self.__name, 'Plugins')
        getattr()
