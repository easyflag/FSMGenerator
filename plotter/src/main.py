import os
from libs.PluginManage.PluginManager import PluginManager


def main():
    dir = os.path.dirname(__file__)
    dir = dir.replace('\\', '/') + '/plugins'
    pluginManager = PluginManager()
    pluginManager.setPluginPath(dir)


if __name__ == '__main__':
    main()
