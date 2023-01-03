import sys

from PyQt5.QtWidgets import *
from gui.downtube_guis import BaseView


class Controller:

    def __init__(self):
        self.base_view = BaseView()

    def display_view(self):
        self.base_view.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller()
    controller.display_view()
    app.exec()
