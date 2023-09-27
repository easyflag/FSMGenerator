import os
from libs.PluginManage.PluginSpec import PluginSpec


class PluginManager():
    def __init__(self) -> None:
        self.__pluginPath = ''
        self.__pluginSpecs = []

    def setPluginPath(self, path):
        self.__pluginPath = path
        self._readPluginPath()

    def _readPluginPath(self):
        dirs = os.listdir(self.__pluginPath)
        for dir in dirs:
            if os.path.isfile(dir):
                continue

        spec = PluginSpec()
