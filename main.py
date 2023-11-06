import sys

from PyQt6.QtWidgets import QApplication, QMainWindow

from login import *
from window import *


class MyWindow(QMainWindow, Ui_Window):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)


class MyLogin(QMainWindow, Ui_Login):
    def __init__(self, parent=None):
        super(MyLogin, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('windows')
    my_login = MyLogin()
    my_window = MyWindow()
    my_login.show()
    my_login.btn_login.clicked.connect(my_window.show)
    my_login.btn_login.clicked.connect(my_login.close)
    sys.exit(app.exec())
