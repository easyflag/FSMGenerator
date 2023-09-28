import importlib
import yaml


class PluginSpec():
    def __init__(self) -> None:
        self.__name = ''
        self.__modulePath = ''
        self.__pluginInstance = None

    @property
    def name(self):
        return self.__name

    def readDescription(self, descFile):
        with open(descFile, "+r") as f:
            dict = yaml.safe_load(f)
            if 'Name' not in dict.keys():
                return False
            self.__name = dict['Name']

            if 'ModulePath' not in dict.keys():
                return False
            self.__modulePath = dict['ModulePath']

    def loadPluginClass(self):
        module = importlib.import_module(self.__modulePath)
        pluginClass = getattr(module, self.__name + 'Plugin')
        self.__pluginInstance = pluginClass()

    def initPluginClass(self):
        self.__pluginInstance.initialize()
