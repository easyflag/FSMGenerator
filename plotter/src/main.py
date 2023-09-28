import os
import sys

from PySide2 import QtWidgets

from libs.ExtensionSystem.PluginManager import PluginManager


def main():
    app = QtWidgets.QApplication(sys.argv)

    pluginManager = PluginManager()
    path = os.path.join(os.path.dirname(__file__), 'plugins')
    pluginManager.setPluginPath(path)
    pluginManager.loadPlugins()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
