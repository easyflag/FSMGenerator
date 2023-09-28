from PySide2.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def initialize(self):
        self.resize(800, 600)

        self.show()
