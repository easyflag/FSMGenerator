import os

from libs.ExtensionSystem.PluginSpec import PluginSpec


class PluginManager():
    def __init__(self):
        self.__pluginPath = ''
        self.__pluginSpecs = []

    @property
    def pluginSpecs(self):
        return self.__pluginSpecs

    def setPluginPath(self, path):
        self.__pluginPath = path
        self._readPluginPath()

    def loadPlugins(self):
        for spec in self.__pluginSpecs:
            spec.loadPluginClass()
        for spec in self.__pluginSpecs:
            spec.initPluginClass()

    def _readPluginPath(self):
        names = os.listdir(self.__pluginPath)
        for name in names:
            path = os.path.join(self.__pluginPath, name)
            if os.path.isfile(path):
                continue
            dirs = os.listdir(path)
            for dir in dirs:
                file = os.path.join(path, dir)
                if os.path.isfile(file) and dir == 'desc.yaml':
                    spec = PluginSpec()
                    spec.readDescription(file)
                    self.__pluginSpecs.append(spec) 
                    break
