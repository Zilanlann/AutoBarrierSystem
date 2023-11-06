import sys

from PyQt6.QtCore import QThread, pyqtSignal, QMutex, QWaitCondition, QMutexLocker
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox

from login import *
from window import *
from passdialog import *
from link_serial import *
from db_connections import *


class MyThread(QThread):
    """子线程，用于持续检测IC卡"""
    card_status = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mutex = QMutex()  # 互斥锁，用于线程同步
        self.cond = QWaitCondition()  # 等待条件，用于线程暂停和恢复

    def run(self):
        while True:
            with QMutexLocker(self.mutex):
                # 检测IC卡
                rfid_tag = get_card_id(ser)
                # rfid_tag = "FFFFF"
                self.tmp = determine_entry_or_exit(rfid_tag)
                self.card_status.emit(self.tmp)
                sleep(0.5)


class PassDialog(QMainWindow, Ui_PassDialog):
    """密码修改界面"""

    def __init__(self, parent=None):
        super(PassDialog, self).__init__(parent)
        self.setupUi(self)
        self.setup_ui()

    def setup_ui(self):
        self.ConfirmPushButton.clicked.connect(self.modify_password)
        self.CancelPushButton.clicked.connect(self.close)

    def modify_password(self):
        """密码修改"""
        username = self.username.text()
        old_password = self.oldpassword.text()
        new_password = self.newpassword.text()
        result = change_password(username, old_password, new_password)
        if result == 1:
            QMessageBox.information(self, "提示", "密码修改成功！")
            my_login.show()
            my_window.close()
            pass_dialog.close()

        elif result == 0:
            QMessageBox.information(self, "提示", "旧密码错误，请重新输入！")
        else:
            QMessageBox.information(self, "提示", "该用户不存在！")


def modify_password():
    """打开密码修改界面"""
    pass_dialog.show()


class MyWindow(QMainWindow, Ui_MainWindow):
    """主程序窗口"""
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.thread = None
        self.thread_running = False  # 标记线程是否正在运行
        self.setupUi(self)
        self.setup_ui()

    def setup_ui(self):
        self.addcar.clicked.connect(self.add_car)
        self.mpass.clicked.connect(modify_password)
        self.runsys.clicked.connect(self.start_thread)

    def add_car(self):
        """将文本框里输入的值车牌号与检测到的IC卡号一起存入数据库"""
        QMessageBox.information(self, "提示", "请将IC卡放置到检测区域，两个小灯全闪烁即为添加成功！")
        rfid_tag = get_card_id(ser)
        # sleep(2)
        # rfid_tag = "FFFFFF"
        license_plate = self.carLineEdit.text()
        add_new_car(license_plate, rfid_tag)
        QMessageBox.information(self, "提示", "车辆添加成功！")
        send(ser, "A1#")
        sleep(0.5)
        send(ser, "A0#")

    def setup_thread(self):
        self.thread = MyThread()
        self.thread.card_status.connect(self.act)
        self.thread_running = True

    def act(self, status):
        """信号槽触发函数，根据信号判断车辆进入驶出，并弹出对应消息框"""
        if status == -1:
            send(ser, "A1#")
            sleep(0.2)
            send(ser, "A0#")
            QMessageBox.information(self, "提示", f"车辆进入，道闸开启，开始计费")
        elif status == -2:
            QMessageBox.information(self, "提示", "请先注册车辆！！！")
        else:
            send(ser, "A1#")
            sleep(0.2)
            send(ser, "A0#")
            QMessageBox.information(self, "提示", f"车辆离开，道闸关闭，收费{status}元")

    def start_thread(self):
        """开启子线程"""
        QMessageBox.information(self, "提示", "道闸控制系统已开启，将持续检测汽车通行")
        if self.thread_running:
            self.thread.start()
        if not self.thread_running:
            self.setup_thread()
            self.thread.start()


class MyLogin(QMainWindow, Ui_Login):
    """登录窗口"""
    def __init__(self, parent=None):
        super(MyLogin, self).__init__(parent)
        self.setupUi(self)
        self.setup_ui()

    def setup_ui(self):
        # 绑定按钮点击事件
        self.btn_login.clicked.connect(self.check_login)

    def check_login(self):
        username = self.UserLineEdit.text()
        password = self.PasswordLineEdit.text()
        result = authenticate_user(username, password)
        if result == 1:
            my_window.show()
            my_login.close()
        elif result == 0:
            QMessageBox.information(self, "提示", "密码错误，请重新输入！")
        else:
            QMessageBox.information(self, "提示", "该用户不存在！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyle('windows')
    my_login = MyLogin()
    my_window = MyWindow()
    pass_dialog = PassDialog()
    ser = init_serial()
    delete_all()  # 演示需要
    init_table()
    # 添加默认管理员用户
    add_user("admin", "admin")
    my_login.show()
    sys.exit(app.exec())
