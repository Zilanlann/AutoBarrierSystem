import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from qfluentwidgets import MessageBox, MessageBoxBase, MessageDialog

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

    def setup_ui(self):
        # 按钮绑定函数
        self.btn_login.clicked.connect(self.checkLogin)

    def checkLogin(self):
        username = self.UserLineEdit.text()
        password = self.PasswordLineEdit.text()
        result = authenticate_user(username, password)
        if result == 1:
            my_window.show()
            my_login.close()
        elif result == 0:
            QMessageBox.information(self, "提示", "该用户不存在")
            # MessageBox.show(self)
            # MessageBox.nativeEvent(self, 1, "该用户不存在")
        else:
            # MessageBox.show(self)
            QMessageBox.information(self, "提示", "该用户不存在")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('windows')
    my_login = MyLogin()
    my_window = MyWindow()
    my_login.show()
    sys.exit(app.exec())
