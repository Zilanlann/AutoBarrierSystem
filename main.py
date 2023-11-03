import sys

from PyQt6.QtWidgets import QApplication, QMainWindow

from window import *


class MyWindow(QMainWindow, Ui_Window):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('windows')
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec())
